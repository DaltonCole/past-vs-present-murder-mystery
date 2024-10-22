import logging
from typing import Dict

from bonus_points.scripts.get_team_bonus_points import get_team_bonus_points
from teams.models import Team, TeamToClue
from teams.scripts.get_team_clues_in_order import get_team_clues_in_order

logger = logging.getLogger(__name__)


def team_to_clue_to_clue_context(team_to_clue: TeamToClue) -> Dict[str, str]:
    '''Convert TeamToClue to a view that can be used by the html template

    Args:
        team_to_clue: The clue to make readable

    Returns:
        {
            'clue-type': Either 'location' or 'person',
            'hint1': 'First hint',
            'hint2': hint as string or empty string if not unlocked,
            'hint3': hint as string or empty string if not unlocked,
        }
    '''
    if team_to_clue.video_clue is not None:
        clue = team_to_clue.video_clue
        return {
                'clue-type': 'location',
                'hint1': clue.location_hint1,
                'hint2': clue.location_hint2 if team_to_clue.location_hints > 0 else '',
                'hint3': clue.location_hint3 if team_to_clue.location_hints > 1 else '',
                }
    else:
        clue = team_to_clue.text_clue
        reference_char = clue.character_id

        location_hint1 = clue.descriptor1_flavor_text.flavor_text.format(**{'char': reference_char, 'description': reference_char.descriptor1})
        location_hint2 = clue.descriptor2_flavor_text.flavor_text.format(**{'char': reference_char, 'description': reference_char.descriptor2})
        location_hint3 = clue.descriptor3_flavor_text.flavor_text.format(**{'char': reference_char, 'description': reference_char.descriptor3})
        location_hint3 += '\n'
        location_hint3 += clue.occupation_flavor_text.flavor_text.format(**{'char': reference_char, 'occupation': reference_char.occupation})

        return {
                'clue-type': 'person',
                'hint1': location_hint1,
                'hint2': location_hint2 if team_to_clue.location_hints > 0 else '',
                'hint3': location_hint3 if team_to_clue.location_hints > 1 else '',
                }
