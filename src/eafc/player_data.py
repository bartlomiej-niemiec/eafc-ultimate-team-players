from dataclasses import dataclass


class PlayerDataKeys:
    PlayerID = "id"
    Name = "name"
    Position = "position"
    AltPosition = "alt position"
    Price = "price"
    Country = "Country"
    League = "League"
    Club = "Club"
    OverallRating = "overall rating"


@dataclass
class PlayerData:
    id: str
    name: str
    position: str
    alt_position: str
    price: int
    country: str
    league: str
    club: str
    overall_rating: int


def create_player_data_from_dict(player_data_dict):
    return PlayerData(
        id=player_data_dict[PlayerDataKeys.PlayerID],
        name=player_data_dict[PlayerDataKeys.Name],
        position=player_data_dict[PlayerDataKeys.Position],
        alt_position=player_data_dict[PlayerDataKeys.AltPosition],
        price=player_data_dict[PlayerDataKeys.Price],
        league=player_data_dict[PlayerDataKeys.League],
        club=player_data_dict[PlayerDataKeys.Club],
        overall_rating=player_data_dict[PlayerDataKeys.OverallRating]
    )
