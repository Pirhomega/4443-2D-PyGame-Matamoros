from helper_module import load_colors

colors = load_colors('colors.json')

with open("output.txt", 'w') as output:
    for color in colors:
        output.write(color)
        output.write('\n')
