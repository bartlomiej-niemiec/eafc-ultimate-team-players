class PlayerDataTemplateFactory:

    @classmethod
    def create(cls, with_stats):
        template_dict = GeneralPlayerData.get_dict_template()
        if with_stats:
            template_dict.update(CommonPosStats.get_dict_template())
            template_dict.update(GkPosStats.get_dict_template())

        return template_dict


class GeneralPlayerData:
    Name = "Name"
    Version = "Version"
    Club = "Club"
    League = "League"
    Nationality = "Nationality"
    AltPos = "Alt Pos."
    SkillMoves = "Skill Moves"
    WeakFoot = "Weak Foot"
    Foot = "Foot"
    AttWR = "Att W/R"
    DefWR = "Def W/R"
    Age = "Age"
    Height = "Height"
    Weight = "Weight"
    BodyType = "Body Type"
    Added = "Added"
    Price = "Price"
    Position = "Position"
    ID = "ID"
    OverallRating = "Overall Rating"
    FutwizLink = "Futwiz Link"

    @classmethod
    def get_dict_template(cls):
        return {
            getattr(cls, x): "" for x in dir(cls) if "__" not in x and isinstance(getattr(cls, x), str)
        }


class CommonPosStats:
    PAC = "PAC"
    AcceleRATE = "AcceleRATE"
    Acceleration = "Acceleration"
    SprintSpeed = "Sprint Speed"
    SHO = "SHO"
    Positioning = "Positioning"
    Finishing = "Finishing"
    ShotPower = "Shot Power"
    LongShots = "Long Shots"
    Volleys = "Volleys"
    Penalties = "Penalties"
    PAS = "PAS"
    Vision = "Vision"
    Crossing = "Crossing"
    FKAcc = "FK. Acc."
    ShortPass = "Short Pass"
    LongPass = "Long Pass"
    Curve = "Curve"
    DRI = "DRI"
    Agility = "Agility"
    Balance = "Balance"
    Reactions = "Reactions"
    BallControl = "Ball Control"
    Dribbling = "Dribbling"
    Composure = "Composure"
    DEF = "DEF"
    Interceptions = "Interceptions"
    HeadingAcc = "Heading Acc."
    DefAwareness = "Def. Awareness"
    StandTackle = "Stand Tackle"
    SlideTackle = "Slide Tackle"
    PHY = "PHY"
    Jumping = "Jumping"
    Stamina = "Stamina"
    Strength = "Strength"
    Aggression = "Aggression"
    PlayStylesPlus = "PlayStyles+"
    PlayStyles = "PlayStyles"

    @classmethod
    def get_dict_template(cls):
        return {
            getattr(cls, x): "" for x in dir(cls) if "__" not in x and isinstance(getattr(cls, x), str)
        }


class GkPosStats:
    DIV = "DIV"
    GKDiving = "GK. Diving"
    REF = "REF"
    GKReflexes = "GK. Reflexes"
    HAN = "HAN"
    GKHandling = "GK. Handling"
    SPD = "SPD"
    KIC = "KIC"
    GKKicking = "GK. Kicking"
    POS = "POS"
    GKPos = "GK. Pos"

    @classmethod
    def get_dict_template(cls):
        return {
            getattr(cls, x): "" for x in dir(cls) if "__" not in x and isinstance(getattr(cls, x), str)
        }
