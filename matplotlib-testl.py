import matplotlib.pyplot as plt
w = 4
h = 3
d = 70
plt.figure(figsize=(w, h), dpi=d)
x = [[3, 4, 5],
     [2, 3, 4],
     [1, 2, 3]]

color_map = plt.imshow(x)
color_map.set_cmap("Blues_r")
plt.colorbar()
plt.show()

plt.savefig("out.png")