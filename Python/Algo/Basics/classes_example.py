class Music():
    artists = []

    def add_Artist(self, name, kind):
        info = {
            "name" : name,
            "kind" : kind,
        }
        return self.artists.append(info)
    def get_Info(self):
        return self.artists


obj = Music()
obj.add_Artist("U2", "Rock")
obj.add_Artist("Kyo", "Pop")
obj.add_Artist("Babymetal", "HardMetal")
obj.add_Artist("RadWimps", "Jap")
obj.add_Artist("Mozart", "Classique")

print(obj.get_Info())

