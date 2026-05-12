import re

with open('stats/templates/stats/standings.html', 'r') as f:
    content = f.read()

# Increase container min-width
content = content.replace('min-w-[1400px]', 'min-w-[1500px]')

# Increase card padding and spacing
content = content.replace('p-3', 'p-4')
content = content.replace('gap-2', 'gap-4')
content = content.replace('w-24 sm:w-28', 'w-32 sm:w-36')
content = content.replace('text-xs', 'text-sm')
content = content.replace('text-sm font-black', 'text-base font-black')
content = content.replace('w-6 h-6', 'w-8 h-8')
content = content.replace('w-10 h-10', 'w-12 h-12') # Finals logos
content = content.replace('text-xl font-black', 'text-2xl font-black') # Finals scores

with open('stats/templates/stats/standings.html', 'w') as f:
    f.write(content)
