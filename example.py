from badosz import Badosz

b = Badosz("")
b.init_nsfw()


print(b.endpoints)
print(b.flip("Hi"))
print(b.ass)
print(b.vaporwave("Love you").get_file())
print(b.vaporwave("Love you").get_discord_file())
