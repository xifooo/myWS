class PartyAnimal:
    x,name = 0,''
    def __init__(self,z) -> None:
        self.name = z

    def party(self):
        self.x = self.x + 1
        print(self.name, "party count", self.x)


s = PartyAnimal("Sally")
s.party()

j = PartyAnimal("Jim")
j.party()
s.party()

"""_summary_
s和j虽属于同一类, 但s.x和j.x是分开的
"""
    