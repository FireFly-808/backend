from pyrovision.datasets import OpenFire

test_set = OpenFire(root="openfire", train=True, download=True)
print(f"Train Set Length: {len(test_set)}")

for i in range(len(test_set)):
    img, target = test_set[i]
    print(f"i: {i}, \nimg.size: {img.size}, \ntarget: {target}\n")
    if i == 3:
        break
