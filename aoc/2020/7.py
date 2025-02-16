#!/usr/bin/env python3

import re

input = """bright gray bags contain 2 bright gold bags, 5 dull lavender bags.
pale olive bags contain 1 bright yellow bag, 1 mirrored salmon bag.
mirrored magenta bags contain 4 shiny turquoise bags, 2 bright gold bags, 4 plaid fuchsia bags, 4 wavy lime bags.
shiny blue bags contain 3 dim plum bags, 4 bright blue bags, 5 plaid fuchsia bags.
dotted beige bags contain 5 faded bronze bags, 1 posh olive bag, 5 dark magenta bags, 2 plaid lime bags.
drab tomato bags contain 4 faded fuchsia bags, 4 plaid beige bags, 4 clear red bags.
drab blue bags contain 3 light beige bags, 4 dark gray bags.
striped beige bags contain 1 wavy coral bag, 5 light salmon bags, 5 dark black bags.
dull gold bags contain 5 light gold bags, 4 bright silver bags.
wavy red bags contain 4 bright gray bags, 1 striped green bag.
pale white bags contain 2 plaid fuchsia bags, 3 shiny blue bags, 1 pale black bag, 3 dull purple bags.
bright orange bags contain 5 dim bronze bags.
plaid yellow bags contain 3 light beige bags.
clear red bags contain 2 bright white bags, 5 light orange bags, 3 clear purple bags.
light tomato bags contain 1 plaid fuchsia bag, 5 dark gray bags, 2 striped tan bags, 5 striped lavender bags.
pale yellow bags contain 3 clear indigo bags.
shiny red bags contain 5 bright violet bags, 2 striped cyan bags, 2 bright silver bags, 5 clear indigo bags.
bright maroon bags contain 2 posh aqua bags, 1 plaid purple bag, 5 dull lavender bags, 4 faded turquoise bags.
dark crimson bags contain 1 plaid chartreuse bag.
pale red bags contain 1 faded lavender bag.
shiny lavender bags contain 2 light orange bags.
dotted blue bags contain 3 clear turquoise bags, 2 shiny silver bags.
bright lime bags contain 5 mirrored plum bags, 2 dim blue bags, 4 light brown bags, 2 vibrant lavender bags.
bright lavender bags contain 5 posh gray bags.
faded purple bags contain 5 muted tan bags, 2 bright salmon bags, 2 shiny olive bags.
pale aqua bags contain 4 clear black bags, 4 posh indigo bags.
wavy cyan bags contain 5 faded green bags, 1 wavy lime bag.
dull maroon bags contain 5 light indigo bags, 1 clear purple bag, 3 dark salmon bags.
muted fuchsia bags contain 5 dotted silver bags, 4 plaid tomato bags, 2 drab olive bags, 4 vibrant tomato bags.
clear salmon bags contain 3 faded tomato bags, 1 dull crimson bag.
drab maroon bags contain 4 dotted blue bags, 1 dotted violet bag.
posh blue bags contain 3 dotted bronze bags, 5 shiny chartreuse bags, 4 vibrant tan bags.
shiny gold bags contain 1 plaid tan bag, 3 light beige bags, 1 posh brown bag.
light lavender bags contain 3 posh maroon bags, 2 plaid beige bags, 1 dark gray bag, 5 muted bronze bags.
pale violet bags contain 5 dull beige bags, 3 clear orange bags.
bright gold bags contain no other bags.
wavy maroon bags contain 4 faded olive bags.
wavy salmon bags contain 1 posh indigo bag, 1 clear fuchsia bag.
vibrant orange bags contain 3 plaid tan bags, 4 dotted blue bags, 3 bright gold bags, 3 bright white bags.
vibrant green bags contain 5 muted indigo bags, 4 muted aqua bags, 1 muted plum bag, 3 posh salmon bags.
striped tan bags contain 1 plaid beige bag, 4 shiny bronze bags, 5 muted bronze bags, 4 clear indigo bags.
wavy silver bags contain 4 muted fuchsia bags, 3 muted indigo bags, 1 vibrant cyan bag.
pale beige bags contain 1 dim lavender bag, 1 clear lime bag, 4 faded lavender bags, 3 dull green bags.
mirrored brown bags contain 1 plaid gray bag, 5 drab plum bags.
faded green bags contain 5 light yellow bags, 2 plaid fuchsia bags, 1 drab magenta bag, 1 muted bronze bag.
posh red bags contain 5 plaid magenta bags, 4 striped brown bags.
wavy turquoise bags contain 2 posh coral bags, 3 faded violet bags, 4 striped green bags.
drab indigo bags contain 2 mirrored red bags, 1 plaid blue bag.
shiny black bags contain 3 clear crimson bags, 4 vibrant purple bags, 2 drab salmon bags.
wavy fuchsia bags contain 4 wavy magenta bags, 5 plaid chartreuse bags, 4 posh salmon bags, 4 dull teal bags.
clear teal bags contain 4 dark aqua bags.
posh tan bags contain 2 clear silver bags, 1 faded coral bag.
plaid lime bags contain 1 wavy lime bag.
vibrant tomato bags contain 5 clear green bags, 3 posh olive bags, 5 mirrored beige bags.
dull crimson bags contain 5 shiny blue bags, 5 dark magenta bags, 4 dim plum bags, 2 light lavender bags.
dotted salmon bags contain 1 light maroon bag, 2 posh aqua bags, 2 light magenta bags.
striped orange bags contain no other bags.
vibrant bronze bags contain 4 shiny black bags, 1 bright crimson bag.
posh black bags contain 4 shiny turquoise bags, 2 muted indigo bags.
dim gray bags contain 2 plaid purple bags, 3 bright blue bags, 2 plaid beige bags.
pale chartreuse bags contain 5 dull beige bags.
wavy green bags contain 2 drab tomato bags, 3 faded yellow bags, 5 posh aqua bags.
striped red bags contain 3 posh green bags, 1 plaid red bag, 2 muted white bags, 4 dull teal bags.
muted black bags contain 4 dark gray bags, 2 plaid fuchsia bags, 4 shiny purple bags, 2 wavy aqua bags.
vibrant gray bags contain 5 drab bronze bags, 2 muted black bags, 2 clear lime bags.
dotted plum bags contain 4 shiny silver bags, 3 light maroon bags, 4 bright white bags.
mirrored salmon bags contain 2 plaid gold bags.
mirrored orange bags contain 3 pale bronze bags.
dark gold bags contain 3 light yellow bags.
muted orange bags contain 5 dark black bags, 2 bright crimson bags, 1 posh bronze bag.
posh aqua bags contain 3 plaid purple bags.
dotted lime bags contain 3 shiny yellow bags, 4 dull brown bags, 2 dark gray bags.
drab lime bags contain 3 wavy beige bags, 3 dull purple bags, 4 clear tan bags, 4 muted indigo bags.
bright blue bags contain 5 plaid teal bags.
light orange bags contain 2 plaid tan bags, 2 striped orange bags, 3 clear indigo bags.
dark chartreuse bags contain 3 muted teal bags, 5 faded tomato bags.
clear gray bags contain 5 bright bronze bags, 1 mirrored cyan bag.
vibrant lime bags contain 4 striped green bags, 5 dotted lavender bags.
light black bags contain 5 dark tan bags, 3 light magenta bags, 2 clear green bags, 4 dull lavender bags.
clear gold bags contain 4 dotted bronze bags.
light aqua bags contain 1 posh chartreuse bag, 4 mirrored silver bags, 1 dotted gray bag.
mirrored tan bags contain 3 bright chartreuse bags, 5 dull olive bags, 2 bright white bags.
faded tomato bags contain 3 faded coral bags, 3 wavy blue bags, 3 light lime bags.
drab chartreuse bags contain 1 shiny red bag, 1 dotted violet bag.
striped tomato bags contain 2 wavy yellow bags.
clear white bags contain 2 drab bronze bags, 3 clear gray bags, 2 posh white bags.
shiny plum bags contain 5 dim plum bags, 1 wavy beige bag, 1 faded fuchsia bag, 3 plaid white bags.
plaid violet bags contain 3 posh coral bags, 5 dim gray bags, 3 dim plum bags, 3 dull purple bags.
dotted magenta bags contain 4 dotted salmon bags.
mirrored cyan bags contain 3 dark salmon bags, 5 muted teal bags, 2 faded white bags, 4 vibrant fuchsia bags.
muted teal bags contain 2 faded violet bags, 4 dull cyan bags.
striped maroon bags contain 1 mirrored olive bag.
mirrored turquoise bags contain 3 plaid fuchsia bags, 3 mirrored cyan bags, 1 dull black bag.
shiny silver bags contain no other bags.
striped green bags contain 1 wavy teal bag, 2 vibrant indigo bags, 2 dark lime bags.
striped silver bags contain 4 bright yellow bags, 5 faded coral bags.
wavy olive bags contain 4 posh gray bags, 5 dark cyan bags.
clear brown bags contain 3 dull lavender bags, 4 dim gold bags.
bright turquoise bags contain 3 faded lavender bags, 3 posh silver bags.
muted tan bags contain 4 dim plum bags, 2 faded coral bags.
dull green bags contain 1 shiny plum bag, 1 drab fuchsia bag, 5 dark white bags, 3 drab magenta bags.
drab yellow bags contain 5 posh silver bags, 2 clear violet bags, 4 dull teal bags, 2 dotted salmon bags.
plaid aqua bags contain 2 faded beige bags.
vibrant chartreuse bags contain 2 wavy olive bags, 3 dotted salmon bags.
light chartreuse bags contain 2 muted orange bags, 3 dotted black bags, 2 striped lavender bags, 4 striped red bags.
vibrant tan bags contain 1 bright violet bag, 1 clear magenta bag, 4 dark orange bags.
posh turquoise bags contain 5 bright gold bags, 3 striped violet bags.
dotted fuchsia bags contain 5 faded lavender bags, 2 bright crimson bags, 5 muted yellow bags.
dark turquoise bags contain 2 vibrant indigo bags, 5 dull tan bags.
dotted chartreuse bags contain 5 pale red bags.
light lime bags contain 4 bright gold bags, 5 shiny silver bags, 3 posh brown bags, 3 striped orange bags.
mirrored teal bags contain 5 striped silver bags, 5 posh cyan bags, 4 light tomato bags, 4 dim gray bags.
vibrant turquoise bags contain 2 drab plum bags, 4 dark blue bags, 2 dim violet bags, 2 plaid blue bags.
clear blue bags contain 1 wavy indigo bag, 3 dotted yellow bags, 5 drab plum bags, 5 posh white bags.
striped blue bags contain 1 wavy blue bag, 1 striped indigo bag, 4 dull black bags, 3 muted silver bags.
muted silver bags contain 4 muted yellow bags, 1 plaid silver bag, 1 light lavender bag, 1 dotted blue bag.
dotted indigo bags contain 5 clear tomato bags, 4 bright magenta bags, 5 dark crimson bags.
vibrant teal bags contain 3 striped lavender bags, 4 wavy beige bags, 2 dull indigo bags.
striped chartreuse bags contain 5 clear silver bags, 3 drab yellow bags, 5 striped indigo bags, 1 faded turquoise bag.
dotted violet bags contain 5 dark plum bags, 5 dark white bags.
light brown bags contain 3 faded tomato bags, 5 dark bronze bags, 3 shiny turquoise bags, 2 striped violet bags.
posh indigo bags contain 2 vibrant coral bags, 2 wavy maroon bags, 4 drab coral bags, 2 clear fuchsia bags.
drab violet bags contain 5 drab tomato bags, 1 light silver bag, 5 wavy beige bags.
plaid plum bags contain 1 dull magenta bag, 3 dark black bags.
dotted orange bags contain 5 mirrored crimson bags.
dotted teal bags contain 3 clear silver bags.
vibrant brown bags contain 5 vibrant indigo bags.
clear orange bags contain 1 clear turquoise bag.
bright magenta bags contain 1 dark orange bag, 2 dotted purple bags, 1 mirrored white bag, 5 vibrant yellow bags.
clear tan bags contain 2 striped orange bags.
dotted brown bags contain 2 mirrored coral bags, 4 wavy magenta bags, 2 pale purple bags, 1 drab black bag.
vibrant plum bags contain 1 dotted teal bag.
light indigo bags contain 5 light black bags, 1 vibrant purple bag, 3 muted olive bags, 4 mirrored brown bags.
bright chartreuse bags contain 3 dull lime bags.
clear turquoise bags contain 4 pale black bags, 5 plaid purple bags, 4 bright gold bags.
dim crimson bags contain 3 wavy lime bags.
pale tan bags contain 3 mirrored white bags, 3 drab bronze bags, 2 drab black bags.
plaid gold bags contain 5 striped orange bags.
striped crimson bags contain 1 muted brown bag, 4 drab red bags, 1 faded crimson bag.
clear lavender bags contain 1 bright salmon bag, 2 clear teal bags, 4 drab plum bags.
dark maroon bags contain 2 striped purple bags, 1 bright aqua bag, 3 faded white bags, 5 bright yellow bags.
drab gray bags contain 5 posh silver bags, 2 bright chartreuse bags, 2 dim purple bags, 5 faded brown bags.
faded olive bags contain 2 shiny turquoise bags, 5 drab green bags, 4 light maroon bags.
muted gray bags contain 2 dim maroon bags, 5 muted tan bags, 3 faded salmon bags, 5 faded white bags.
posh violet bags contain 2 faded crimson bags.
shiny white bags contain 1 dark chartreuse bag, 5 posh green bags.
mirrored indigo bags contain 5 clear purple bags, 3 dark turquoise bags, 3 clear aqua bags, 2 bright gray bags.
dark brown bags contain 4 wavy gold bags.
muted tomato bags contain 4 clear violet bags.
striped black bags contain 4 plaid white bags, 3 dull tan bags.
shiny crimson bags contain 2 plaid teal bags.
bright coral bags contain 2 clear plum bags, 2 faded orange bags, 3 mirrored silver bags.
dark yellow bags contain 1 plaid olive bag, 3 dotted white bags.
faded beige bags contain 5 posh aqua bags, 1 pale purple bag.
wavy magenta bags contain 3 dull yellow bags, 5 faded cyan bags.
wavy bronze bags contain 5 dull lime bags.
dim lavender bags contain 3 plaid red bags, 3 bright brown bags.
dim indigo bags contain 3 dim violet bags, 4 bright silver bags.
posh green bags contain 4 drab white bags, 3 plaid tan bags, 1 light orange bag.
pale gray bags contain 1 muted indigo bag, 2 dotted fuchsia bags.
mirrored gold bags contain 2 striped beige bags, 3 bright plum bags.
striped white bags contain 5 dark blue bags, 5 dotted purple bags, 4 clear maroon bags.
drab cyan bags contain 3 dotted white bags.
vibrant aqua bags contain 4 posh yellow bags, 1 drab tomato bag.
light gold bags contain 2 vibrant purple bags, 5 light black bags.
dotted yellow bags contain 5 striped lavender bags, 2 posh aqua bags, 2 clear green bags, 2 dull green bags.
vibrant cyan bags contain 2 dark gray bags, 2 dark lavender bags, 1 striped red bag, 2 striped indigo bags.
posh yellow bags contain 3 wavy olive bags, 2 bright gray bags, 2 posh gray bags, 2 vibrant white bags.
faded salmon bags contain 4 plaid beige bags, 1 drab teal bag.
bright purple bags contain 1 faded white bag, 3 plaid teal bags, 3 light lime bags, 1 pale purple bag.
dotted purple bags contain 3 mirrored salmon bags, 3 drab olive bags.
plaid red bags contain 5 faded violet bags, 5 dotted white bags.
vibrant maroon bags contain 3 faded green bags, 3 bright chartreuse bags, 4 clear orange bags, 2 dim tomato bags.
clear crimson bags contain 1 vibrant purple bag, 5 light beige bags, 5 vibrant olive bags.
clear cyan bags contain 1 posh plum bag, 2 vibrant chartreuse bags, 5 plaid silver bags.
vibrant salmon bags contain 2 striped brown bags.
striped olive bags contain 2 muted indigo bags.
dim turquoise bags contain 3 striped violet bags, 1 wavy blue bag.
bright brown bags contain 1 shiny yellow bag.
mirrored tomato bags contain 1 bright violet bag, 1 faded green bag, 3 dotted gray bags, 3 muted silver bags.
dark green bags contain 1 dull olive bag.
wavy white bags contain 4 bright silver bags, 5 vibrant tomato bags, 2 vibrant salmon bags, 4 clear tomato bags.
shiny green bags contain 1 dotted white bag.
dotted aqua bags contain 1 faded lavender bag, 1 pale coral bag, 1 clear silver bag.
shiny aqua bags contain 1 plaid white bag, 4 clear lime bags.
dark lavender bags contain 3 bright aqua bags, 3 mirrored salmon bags, 5 pale red bags, 1 pale purple bag.
dull violet bags contain 5 wavy gold bags, 1 shiny cyan bag, 5 plaid beige bags.
drab tan bags contain 2 drab crimson bags, 1 drab cyan bag, 5 striped tan bags, 3 dotted fuchsia bags.
plaid turquoise bags contain 1 posh silver bag, 4 posh turquoise bags, 5 posh tan bags.
pale lavender bags contain 3 plaid gold bags, 5 pale gray bags, 4 dotted plum bags, 3 mirrored crimson bags.
clear indigo bags contain 5 pale purple bags.
wavy purple bags contain 3 bright yellow bags, 1 wavy gold bag, 3 light lavender bags.
shiny salmon bags contain 3 light orange bags.
mirrored crimson bags contain 4 dull salmon bags, 4 light yellow bags, 3 dark gray bags, 4 dotted blue bags.
plaid chartreuse bags contain 2 shiny turquoise bags.
pale orange bags contain 2 muted lavender bags.
dark cyan bags contain 5 bright lavender bags, 3 wavy black bags, 2 shiny plum bags, 3 dim aqua bags.
dim brown bags contain 1 shiny yellow bag, 2 posh plum bags, 3 muted black bags, 4 light white bags.
pale blue bags contain 1 faded cyan bag, 3 faded crimson bags, 1 wavy indigo bag, 3 dark plum bags.
vibrant red bags contain 5 plaid aqua bags, 2 clear fuchsia bags.
dark salmon bags contain 4 striped violet bags.
bright black bags contain 1 faded silver bag.
vibrant white bags contain 2 vibrant yellow bags, 3 shiny plum bags.
muted violet bags contain 4 pale lavender bags, 4 pale purple bags.
wavy coral bags contain 5 vibrant tomato bags.
striped salmon bags contain 3 dull magenta bags.
faded blue bags contain 2 bright salmon bags, 2 clear salmon bags, 4 striped indigo bags.
dim violet bags contain 1 striped brown bag, 5 bright blue bags, 4 bright bronze bags, 5 dull salmon bags.
faded chartreuse bags contain 2 muted tan bags, 1 plaid aqua bag, 4 dotted white bags.
posh silver bags contain 4 dull salmon bags.
dim red bags contain 1 faded black bag, 2 dark aqua bags, 2 drab crimson bags, 5 dotted aqua bags.
dull lime bags contain 3 pale indigo bags, 5 bright gold bags, 5 light orange bags.
striped fuchsia bags contain 3 clear violet bags, 2 light fuchsia bags, 1 plaid red bag, 3 wavy aqua bags.
vibrant lavender bags contain 1 dark teal bag, 1 dark beige bag, 4 dark cyan bags.
dark gray bags contain 5 drab magenta bags, 3 muted bronze bags, 5 posh gray bags, 2 shiny silver bags.
drab lavender bags contain 4 pale indigo bags, 4 bright salmon bags, 3 posh aqua bags, 4 bright lavender bags.
mirrored white bags contain 3 striped black bags.
bright aqua bags contain 4 plaid tomato bags, 3 clear fuchsia bags, 1 light silver bag.
dark silver bags contain 3 bright tomato bags.
drab fuchsia bags contain 5 dotted plum bags, 2 posh aqua bags, 2 clear red bags, 1 dark gray bag.
bright teal bags contain 3 vibrant tan bags.
striped indigo bags contain 5 wavy plum bags, 2 wavy lavender bags, 4 mirrored beige bags, 4 clear green bags.
dark white bags contain 4 striped brown bags, 4 plaid teal bags, 2 posh brown bags, 2 wavy blue bags.
mirrored maroon bags contain 2 clear cyan bags, 4 shiny aqua bags.
wavy tan bags contain 5 bright maroon bags, 1 clear teal bag.
wavy lime bags contain 3 pale purple bags, 5 plaid teal bags, 5 bright gold bags, 3 clear turquoise bags.
dark plum bags contain 1 dotted orange bag.
posh cyan bags contain 1 light lavender bag, 1 dark orange bag, 2 dull lime bags.
pale crimson bags contain 3 faded fuchsia bags, 4 drab orange bags.
clear yellow bags contain 4 posh tan bags.
striped yellow bags contain 2 muted red bags, 1 light silver bag, 5 mirrored chartreuse bags.
clear silver bags contain 2 dull lavender bags, 3 faded fuchsia bags.
drab red bags contain 3 clear orange bags.
dotted turquoise bags contain 4 bright lavender bags.
striped purple bags contain 1 shiny plum bag, 2 clear orange bags, 3 mirrored turquoise bags, 3 striped orange bags.
striped gray bags contain 1 posh silver bag.
clear purple bags contain 4 muted bronze bags, 3 shiny silver bags, 4 pale salmon bags, 3 plaid fuchsia bags.
light gray bags contain 5 dark fuchsia bags.
dull tan bags contain 1 plaid fuchsia bag.
muted blue bags contain 5 dark plum bags, 4 wavy chartreuse bags, 2 drab green bags.
dull brown bags contain 1 pale gold bag.
bright fuchsia bags contain 1 pale bronze bag, 2 bright yellow bags, 4 drab gold bags.
plaid purple bags contain no other bags.
drab silver bags contain 3 wavy blue bags, 2 wavy black bags, 2 dark olive bags.
light salmon bags contain 5 wavy plum bags, 4 drab white bags, 5 muted bronze bags, 5 mirrored beige bags.
drab beige bags contain 2 bright silver bags, 1 striped blue bag, 2 wavy white bags, 1 plaid lavender bag.
posh beige bags contain 3 dotted tomato bags, 5 wavy chartreuse bags.
muted cyan bags contain 4 dim bronze bags, 5 muted white bags, 3 pale black bags, 2 shiny silver bags.
dull magenta bags contain 1 posh white bag.
shiny cyan bags contain 1 shiny silver bag, 4 pale salmon bags, 5 faded turquoise bags.
mirrored gray bags contain 4 mirrored red bags, 3 vibrant brown bags.
bright cyan bags contain 1 dotted lavender bag.
dotted crimson bags contain 3 wavy yellow bags, 1 shiny brown bag, 2 striped brown bags, 2 dull yellow bags.
dim chartreuse bags contain 5 shiny purple bags.
muted crimson bags contain 2 striped violet bags, 4 clear tan bags.
dim aqua bags contain 1 mirrored magenta bag, 3 dim beige bags.
wavy aqua bags contain 4 bright gray bags.
bright beige bags contain 4 dotted chartreuse bags.
posh purple bags contain 5 wavy aqua bags, 4 posh coral bags, 3 vibrant chartreuse bags.
shiny fuchsia bags contain 1 shiny olive bag.
wavy beige bags contain 2 pale purple bags, 3 pale indigo bags, 3 plaid purple bags.
wavy crimson bags contain 4 shiny gold bags, 5 bright tomato bags.
pale tomato bags contain 3 faded gold bags, 5 shiny gray bags.
bright silver bags contain 1 dotted white bag.
mirrored chartreuse bags contain 2 muted silver bags.
mirrored aqua bags contain 4 plaid violet bags.
wavy brown bags contain 4 faded beige bags, 4 faded brown bags, 2 mirrored blue bags, 3 clear red bags.
dull purple bags contain 3 plaid fuchsia bags, 1 faded lavender bag.
pale turquoise bags contain 4 mirrored violet bags, 3 faded salmon bags, 5 bright white bags.
dull lavender bags contain 1 faded fuchsia bag.
dull aqua bags contain 1 bright yellow bag.
clear maroon bags contain 1 pale bronze bag, 2 clear aqua bags.
wavy lavender bags contain 4 dotted blue bags.
dull blue bags contain 5 wavy magenta bags.
shiny olive bags contain 4 clear magenta bags, 1 vibrant orange bag.
shiny teal bags contain 5 dotted magenta bags, 2 dark crimson bags, 3 dotted brown bags.
dull teal bags contain 1 dull indigo bag, 4 wavy plum bags, 2 drab plum bags.
dim bronze bags contain 5 striped silver bags, 5 posh green bags.
muted bronze bags contain 4 dotted blue bags, 3 pale purple bags, 5 drab magenta bags.
vibrant violet bags contain 3 dim tan bags, 3 striped lavender bags.
dull turquoise bags contain 1 dim white bag.
pale purple bags contain no other bags.
drab aqua bags contain 4 dull beige bags, 5 clear brown bags, 2 mirrored orange bags, 3 mirrored blue bags.
mirrored beige bags contain 4 posh aqua bags.
pale plum bags contain 4 dull coral bags, 4 pale black bags, 1 posh chartreuse bag.
dotted maroon bags contain 5 faded gold bags, 1 clear blue bag, 4 dark black bags.
muted olive bags contain 5 dim violet bags, 4 dotted white bags, 5 plaid purple bags, 3 vibrant orange bags.
wavy yellow bags contain 4 light beige bags.
plaid salmon bags contain 4 pale black bags, 3 dim bronze bags, 1 dotted gold bag.
faded indigo bags contain 3 plaid purple bags, 5 pale gold bags, 1 wavy beige bag.
pale brown bags contain 2 wavy black bags.
clear olive bags contain 4 vibrant tomato bags.
vibrant gold bags contain 3 dull cyan bags.
dark indigo bags contain 5 bright green bags, 1 dark white bag.
drab gold bags contain 4 clear violet bags, 2 striped indigo bags.
light bronze bags contain 3 shiny coral bags.
vibrant black bags contain 2 light black bags, 5 clear orange bags, 2 clear silver bags.
wavy tomato bags contain 1 faded maroon bag, 1 dim violet bag, 5 posh aqua bags.
wavy orange bags contain 2 striped lime bags, 4 posh turquoise bags, 3 dotted purple bags, 1 wavy gold bag.
dark blue bags contain 1 faded gray bag.
drab magenta bags contain no other bags.
posh crimson bags contain 1 mirrored olive bag, 1 striped tomato bag, 5 vibrant orange bags, 1 drab yellow bag.
mirrored coral bags contain 4 drab purple bags, 4 bright gray bags, 4 plaid turquoise bags, 5 plaid aqua bags.
faded crimson bags contain 3 plaid tan bags, 3 vibrant orange bags, 3 mirrored beige bags, 4 dim plum bags.
dotted tan bags contain 1 wavy beige bag, 2 bright maroon bags.
faded magenta bags contain 1 mirrored tan bag.
light maroon bags contain 4 plaid tan bags, 5 shiny silver bags.
dull chartreuse bags contain 2 dim gold bags, 1 faded blue bag, 1 striped violet bag, 4 drab tomato bags.
plaid white bags contain 2 dark gray bags.
plaid fuchsia bags contain no other bags.
dark red bags contain 2 mirrored bronze bags, 2 pale blue bags, 5 plaid orange bags, 5 clear orange bags.
dark fuchsia bags contain 2 faded green bags, 2 mirrored magenta bags, 3 pale red bags.
dull plum bags contain 2 bright blue bags, 3 drab purple bags, 1 dim plum bag, 2 shiny purple bags.
vibrant crimson bags contain 2 bright plum bags.
clear magenta bags contain 1 drab bronze bag, 2 bright turquoise bags, 2 faded gray bags, 1 dim blue bag.
dull indigo bags contain 5 light magenta bags.
vibrant olive bags contain 3 light yellow bags, 3 mirrored silver bags, 2 plaid white bags, 2 dim beige bags.
striped lavender bags contain 1 dull salmon bag, 1 pale purple bag.
clear lime bags contain 4 dim gold bags.
faded orange bags contain 5 light white bags, 4 shiny bronze bags, 3 plaid silver bags.
posh lime bags contain 2 drab orange bags, 5 wavy beige bags.
posh olive bags contain 5 drab green bags, 2 bright maroon bags, 3 vibrant orange bags.
dim yellow bags contain 1 light silver bag, 5 vibrant gray bags, 4 faded turquoise bags, 2 dark blue bags.
muted red bags contain 2 dim purple bags.
pale salmon bags contain 3 vibrant orange bags.
light beige bags contain 5 clear purple bags, 2 plaid teal bags.
clear tomato bags contain 5 dull cyan bags, 4 dark brown bags.
shiny gray bags contain 3 dark brown bags, 1 shiny bronze bag, 5 posh bronze bags, 4 dark indigo bags.
vibrant fuchsia bags contain 4 wavy olive bags, 5 shiny blue bags, 5 light yellow bags.
shiny violet bags contain 4 dull aqua bags, 1 pale fuchsia bag, 3 mirrored lime bags, 5 dark blue bags.
plaid silver bags contain 1 faded fuchsia bag, 5 dull lavender bags.
light white bags contain 1 plaid magenta bag, 4 striped beige bags.
posh magenta bags contain 5 vibrant chartreuse bags, 3 drab silver bags, 4 striped bronze bags, 4 striped salmon bags.
muted maroon bags contain 2 faded coral bags.
light blue bags contain 3 dotted plum bags, 2 pale salmon bags, 4 striped coral bags, 1 bright lavender bag.
pale teal bags contain 3 faded maroon bags, 5 wavy turquoise bags.
posh gold bags contain 4 vibrant violet bags, 1 drab beige bag.
shiny indigo bags contain 4 drab cyan bags.
wavy teal bags contain 1 light maroon bag, 2 shiny silver bags, 2 bright white bags, 1 pale black bag.
striped cyan bags contain 1 plaid brown bag.
pale black bags contain no other bags.
light green bags contain 2 dark salmon bags, 2 faded tomato bags, 1 wavy blue bag, 1 bright gray bag.
mirrored green bags contain 2 striped salmon bags, 3 shiny black bags.
dim orange bags contain 3 vibrant plum bags, 5 drab crimson bags.
clear chartreuse bags contain 2 posh fuchsia bags, 3 vibrant olive bags.
dull black bags contain 3 posh yellow bags, 5 dark bronze bags, 4 dark aqua bags, 5 dull teal bags.
dotted tomato bags contain 2 faded crimson bags, 5 faded black bags.
faded maroon bags contain 4 pale white bags, 5 posh green bags, 3 wavy black bags, 5 plaid tan bags.
plaid cyan bags contain 3 striped blue bags, 3 wavy teal bags.
dark bronze bags contain 2 clear purple bags.
vibrant purple bags contain 2 striped orange bags, 1 wavy black bag.
dotted silver bags contain 4 faded white bags, 5 dim blue bags, 1 dark white bag.
mirrored yellow bags contain 5 dark black bags.
dim lime bags contain 3 dim lavender bags, 5 shiny gold bags, 5 striped red bags.
faded tan bags contain 4 clear black bags, 3 pale silver bags, 1 muted gold bag.
drab plum bags contain 4 shiny gold bags.
plaid lavender bags contain 3 drab blue bags, 3 faded tomato bags, 5 bright cyan bags.
dark beige bags contain 3 dim indigo bags, 2 plaid white bags.
dotted red bags contain 2 mirrored indigo bags.
dull orange bags contain 3 mirrored cyan bags, 4 shiny gold bags, 5 posh white bags.
striped bronze bags contain 1 drab coral bag, 1 dark teal bag, 5 posh yellow bags.
wavy indigo bags contain 1 drab lavender bag, 2 posh aqua bags, 1 clear brown bag.
light cyan bags contain 3 dim blue bags, 5 dark brown bags, 3 clear bronze bags.
plaid orange bags contain 4 plaid tan bags, 1 posh tomato bag, 1 wavy crimson bag.
faded turquoise bags contain 1 muted bronze bag, 1 wavy gold bag, 4 striped orange bags, 3 bright gold bags.
shiny orange bags contain 1 wavy maroon bag.
light tan bags contain 5 mirrored black bags, 4 dark tan bags.
pale coral bags contain 1 faded coral bag, 4 dotted yellow bags.
faded lavender bags contain 3 vibrant orange bags, 4 pale black bags, 2 posh aqua bags, 5 shiny gold bags.
dull cyan bags contain 3 bright maroon bags, 4 light yellow bags, 4 faded tomato bags.
shiny turquoise bags contain 1 posh gray bag.
faded violet bags contain 5 posh tan bags, 3 dim blue bags.
mirrored bronze bags contain 1 striped silver bag.
dull tomato bags contain 1 dim black bag, 5 wavy olive bags, 1 faded olive bag.
faded red bags contain 2 drab salmon bags, 2 posh aqua bags, 5 posh brown bags.
dark magenta bags contain 1 posh silver bag, 5 bright lavender bags, 4 faded turquoise bags, 5 drab white bags.
light turquoise bags contain 5 dotted turquoise bags, 2 dim plum bags, 2 posh olive bags, 4 mirrored gold bags.
clear green bags contain 3 bright white bags, 2 dark tan bags.
clear coral bags contain 3 clear turquoise bags, 2 striped black bags.
dotted bronze bags contain 5 striped blue bags, 2 striped lavender bags, 4 bright salmon bags, 5 drab maroon bags.
drab salmon bags contain 3 bright blue bags, 4 drab magenta bags.
faded aqua bags contain 2 light magenta bags.
bright violet bags contain 2 wavy indigo bags.
mirrored silver bags contain 5 shiny gold bags.
posh maroon bags contain 1 dark lime bag, 4 plaid gold bags, 4 light magenta bags, 4 dim aqua bags.
striped brown bags contain 5 dull lavender bags.
bright olive bags contain 3 striped coral bags.
drab white bags contain 5 plaid teal bags, 3 shiny silver bags, 3 wavy plum bags, 1 bright white bag.
faded teal bags contain 3 muted blue bags, 2 bright purple bags.
striped plum bags contain 4 plaid turquoise bags, 5 vibrant fuchsia bags.
dark coral bags contain 1 muted salmon bag, 1 mirrored bronze bag, 3 pale maroon bags, 5 dotted coral bags.
drab orange bags contain 1 pale gold bag.
bright tan bags contain 3 pale plum bags, 2 posh yellow bags.
drab brown bags contain 1 plaid red bag, 4 pale tan bags.
posh bronze bags contain 4 dim indigo bags, 4 drab purple bags, 2 dark bronze bags.
mirrored purple bags contain 3 plaid beige bags, 3 bright tomato bags, 3 bright chartreuse bags, 4 wavy crimson bags.
wavy blue bags contain 1 dotted blue bag, 1 pale purple bag, 3 light maroon bags.
dim cyan bags contain 5 faded yellow bags, 2 shiny coral bags, 3 faded black bags, 4 vibrant chartreuse bags.
plaid olive bags contain 1 dim aqua bag, 4 mirrored indigo bags, 4 muted silver bags.
dark orange bags contain 5 faded fuchsia bags, 4 clear purple bags.
drab olive bags contain 1 drab lavender bag.
pale fuchsia bags contain 3 bright green bags, 4 striped red bags, 2 pale brown bags.
shiny chartreuse bags contain 2 striped beige bags, 3 clear tomato bags.
shiny brown bags contain 1 faded maroon bag, 2 muted brown bags, 2 vibrant coral bags.
striped turquoise bags contain 4 pale bronze bags.
dull gray bags contain 4 plaid gray bags.
wavy chartreuse bags contain 2 wavy maroon bags, 4 muted yellow bags.
bright green bags contain 2 dotted orange bags, 4 faded olive bags, 5 wavy beige bags, 1 bright yellow bag.
dark olive bags contain 5 light indigo bags, 5 plaid chartreuse bags, 2 vibrant red bags, 5 dark lime bags.
dark black bags contain 2 dark fuchsia bags, 1 dotted fuchsia bag.
dim purple bags contain 5 posh gray bags, 3 faded lavender bags, 4 bright plum bags, 2 dotted salmon bags.
pale gold bags contain 1 posh silver bag, 4 posh tan bags, 1 bright gold bag, 5 faded gray bags.
pale maroon bags contain 2 drab fuchsia bags, 2 dark fuchsia bags, 5 plaid red bags.
light plum bags contain 1 dim beige bag, 2 light orange bags.
mirrored plum bags contain 5 light white bags, 5 bright tomato bags, 1 dim violet bag.
dim coral bags contain 2 light lime bags, 2 clear tan bags.
faded silver bags contain 4 striped violet bags, 2 mirrored brown bags.
posh salmon bags contain 4 dull plum bags.
shiny purple bags contain 2 posh gray bags.
shiny maroon bags contain 2 vibrant turquoise bags, 4 drab teal bags.
clear beige bags contain 2 mirrored white bags, 1 shiny turquoise bag, 5 faded bronze bags.
muted plum bags contain 2 plaid violet bags.
plaid green bags contain 3 drab white bags, 5 wavy gold bags, 3 bright maroon bags, 1 wavy cyan bag.
faded white bags contain 1 dull cyan bag, 3 dull purple bags, 2 bright brown bags, 4 bright crimson bags.
plaid gray bags contain 3 bright chartreuse bags, 2 plaid tomato bags, 2 dark brown bags.
shiny yellow bags contain 5 drab salmon bags.
mirrored violet bags contain 4 clear fuchsia bags.
plaid beige bags contain 1 pale black bag.
plaid black bags contain 1 dark chartreuse bag.
mirrored fuchsia bags contain 5 light tomato bags, 4 shiny yellow bags, 1 plaid beige bag, 5 muted gold bags.
pale indigo bags contain 1 pale black bag, 5 plaid teal bags.
light magenta bags contain 1 mirrored silver bag, 4 dull salmon bags.
striped teal bags contain 1 dotted lime bag, 3 shiny yellow bags, 3 wavy aqua bags.
dark aqua bags contain 3 drab green bags.
bright red bags contain 5 shiny chartreuse bags, 3 mirrored bronze bags, 1 pale beige bag.
dim teal bags contain 2 shiny yellow bags, 3 drab turquoise bags, 1 striped black bag, 1 vibrant coral bag.
drab crimson bags contain 5 light silver bags, 4 plaid chartreuse bags.
dim silver bags contain 1 striped brown bag, 5 dark black bags, 1 light lime bag.
drab bronze bags contain 1 dotted white bag.
drab teal bags contain 2 dim blue bags, 4 light yellow bags, 5 dark gray bags.
dark teal bags contain 5 posh gray bags, 4 faded green bags, 1 dotted yellow bag, 4 vibrant black bags.
vibrant indigo bags contain 4 faded turquoise bags.
mirrored black bags contain 2 muted bronze bags.
dotted gray bags contain 3 faded cyan bags.
posh plum bags contain 4 dark bronze bags, 3 drab olive bags, 4 dull beige bags, 3 plaid silver bags.
drab black bags contain 1 wavy teal bag.
faded gray bags contain 5 dull lime bags, 4 posh aqua bags.
muted white bags contain 2 shiny lavender bags, 3 wavy olive bags, 4 bright brown bags.
wavy gray bags contain 3 faded lavender bags, 5 posh silver bags.
plaid magenta bags contain 1 shiny silver bag, 3 light silver bags, 5 posh gray bags, 2 faded green bags.
muted coral bags contain 5 dull salmon bags, 4 shiny plum bags.
plaid tomato bags contain 5 dotted blue bags.
dark lime bags contain 1 striped orange bag, 1 pale black bag.
vibrant coral bags contain 1 vibrant yellow bag, 1 plaid magenta bag, 3 pale gray bags, 2 vibrant indigo bags.
drab turquoise bags contain 2 plaid tomato bags, 3 dim indigo bags, 2 shiny tomato bags, 1 plaid red bag.
mirrored red bags contain 5 plaid chartreuse bags.
plaid brown bags contain 5 drab blue bags, 1 mirrored olive bag.
striped gold bags contain 3 vibrant aqua bags, 1 posh plum bag, 1 dotted blue bag, 3 light yellow bags.
drab purple bags contain 2 clear green bags, 4 dull cyan bags, 3 posh tan bags, 5 faded violet bags.
posh chartreuse bags contain 2 pale black bags.
clear violet bags contain 1 dark tomato bag, 4 light lime bags, 4 faded magenta bags.
striped magenta bags contain 5 wavy plum bags, 2 light maroon bags, 4 posh gray bags, 2 shiny silver bags.
muted salmon bags contain 5 muted black bags, 5 vibrant coral bags.
pale silver bags contain 3 light lime bags, 3 dotted orange bags, 4 plaid teal bags.
striped lime bags contain 5 dim tomato bags, 2 clear purple bags, 2 mirrored brown bags.
dull silver bags contain 2 wavy gold bags.
dark violet bags contain 1 dotted plum bag, 5 faded turquoise bags, 4 light salmon bags.
dim black bags contain 4 clear violet bags, 4 posh chartreuse bags, 1 plaid turquoise bag, 1 pale black bag.
shiny beige bags contain 3 dim aqua bags.
plaid tan bags contain no other bags.
faded yellow bags contain 5 vibrant fuchsia bags.
vibrant blue bags contain 2 vibrant olive bags, 4 faded cyan bags.
mirrored lime bags contain 3 mirrored blue bags.
dull white bags contain 5 dark brown bags.
dim tomato bags contain 4 dark violet bags, 5 dotted tan bags, 1 plaid teal bag, 2 shiny plum bags.
pale cyan bags contain 1 dotted coral bag, 4 dim green bags.
light fuchsia bags contain 1 posh aqua bag, 3 posh coral bags.
posh gray bags contain 5 faded green bags, 5 pale indigo bags, 3 plaid fuchsia bags, 4 faded beige bags.
faded cyan bags contain 3 dark bronze bags, 1 wavy plum bag.
plaid bronze bags contain 5 pale silver bags.
dim olive bags contain 2 shiny gray bags.
faded coral bags contain 4 wavy blue bags.
pale lime bags contain 2 dull indigo bags.
dim white bags contain 4 dotted tan bags, 5 dull indigo bags, 5 plaid red bags, 2 faded silver bags.
muted turquoise bags contain 1 drab coral bag.
clear bronze bags contain 5 dark lime bags.
bright plum bags contain 4 faded coral bags, 2 pale indigo bags, 4 drab salmon bags.
posh orange bags contain 2 muted brown bags, 1 light white bag, 2 faded blue bags.
muted chartreuse bags contain 2 pale plum bags, 5 light purple bags.
shiny bronze bags contain 3 faded turquoise bags, 5 wavy lavender bags.
shiny coral bags contain 1 wavy coral bag, 5 mirrored olive bags.
posh lavender bags contain 3 clear gray bags, 5 vibrant white bags.
clear fuchsia bags contain 4 clear indigo bags, 3 wavy lavender bags, 2 wavy teal bags, 1 clear green bag.
bright tomato bags contain 3 posh silver bags, 2 wavy beige bags, 4 plaid white bags.
light yellow bags contain 2 plaid tan bags, 1 plaid purple bag, 3 bright gold bags.
pale magenta bags contain 3 vibrant turquoise bags.
bright bronze bags contain 2 shiny gold bags, 4 striped violet bags, 4 striped orange bags, 3 drab green bags.
faded bronze bags contain 2 dim bronze bags, 4 plaid green bags, 3 light purple bags, 5 striped indigo bags.
plaid coral bags contain 2 vibrant salmon bags, 4 drab coral bags, 5 light tan bags.
dull coral bags contain 2 striped coral bags.
muted purple bags contain 1 bright indigo bag.
light silver bags contain 3 muted olive bags, 5 drab purple bags, 2 drab lavender bags.
muted aqua bags contain 5 dull olive bags, 5 drab cyan bags, 5 pale red bags.
posh white bags contain 4 dim plum bags, 3 wavy blue bags.
dotted olive bags contain 4 light brown bags.
muted lime bags contain 4 pale gold bags, 4 dull tan bags.
vibrant magenta bags contain 3 muted olive bags, 2 drab silver bags, 5 posh purple bags.
dotted coral bags contain 3 striped turquoise bags, 3 plaid magenta bags, 4 muted cyan bags.
drab green bags contain 1 drab salmon bag, 3 vibrant purple bags, 3 shiny gold bags, 1 posh silver bag.
vibrant silver bags contain 5 faded salmon bags.
dull bronze bags contain 3 light plum bags.
striped coral bags contain 1 posh brown bag, 4 drab green bags, 1 pale white bag, 1 posh bronze bag.
dim blue bags contain 2 plaid beige bags, 2 faded gray bags.
mirrored olive bags contain 2 plaid gray bags, 2 vibrant yellow bags, 3 dim magenta bags.
bright salmon bags contain 3 bright yellow bags.
bright crimson bags contain 2 plaid gold bags, 5 bright plum bags.
vibrant yellow bags contain 1 bright chartreuse bag.
plaid indigo bags contain 3 wavy silver bags.
bright indigo bags contain 2 shiny black bags, 1 pale indigo bag.
clear aqua bags contain 2 drab black bags, 3 clear tan bags, 5 drab purple bags, 1 plaid green bag.
posh tomato bags contain 3 posh blue bags.
dim tan bags contain 2 vibrant crimson bags, 4 dark lavender bags, 1 drab orange bag, 1 plaid tomato bag.
dim plum bags contain 3 vibrant orange bags.
posh teal bags contain 1 clear salmon bag, 3 light aqua bags.
muted indigo bags contain 1 mirrored black bag, 1 vibrant purple bag.
dull beige bags contain 4 bright gray bags, 5 pale silver bags.
dotted cyan bags contain 4 bright maroon bags, 5 drab cyan bags, 1 bright tomato bag, 4 plaid aqua bags.
faded fuchsia bags contain 2 light orange bags, 4 clear turquoise bags, 4 pale purple bags, 3 dotted blue bags.
pale bronze bags contain 1 wavy cyan bag, 2 light silver bags, 1 light magenta bag, 3 plaid chartreuse bags.
dim beige bags contain 2 striped lavender bags, 2 wavy teal bags, 1 dim plum bag, 4 bright maroon bags.
muted beige bags contain 4 faded black bags, 4 plaid black bags, 4 clear magenta bags.
dotted lavender bags contain 5 shiny silver bags, 1 plaid gold bag, 2 wavy lavender bags.
pale green bags contain 2 pale gold bags.
drab coral bags contain 1 posh yellow bag, 5 wavy maroon bags, 2 posh chartreuse bags, 2 bright gold bags.
wavy plum bags contain 1 plaid tan bag, 3 pale black bags, 2 wavy lime bags, 5 pale purple bags.
dotted green bags contain 1 dark black bag, 4 vibrant yellow bags.
light violet bags contain 3 faded red bags.
faded gold bags contain 3 clear teal bags, 2 faded magenta bags.
muted magenta bags contain 5 striped black bags.
light red bags contain 3 dark turquoise bags, 2 dim bronze bags.
dim maroon bags contain 1 dull gold bag, 3 posh yellow bags.
dull fuchsia bags contain 5 dotted salmon bags, 5 posh gray bags, 5 dark tan bags, 3 dull salmon bags.
wavy gold bags contain 1 plaid teal bag, 5 light maroon bags.
light coral bags contain 2 mirrored cyan bags, 3 posh salmon bags, 4 faded red bags.
dark tan bags contain 3 wavy cyan bags.
faded plum bags contain 1 dim gold bag, 4 muted crimson bags, 1 mirrored brown bag.
wavy black bags contain 5 clear green bags.
wavy violet bags contain 3 bright brown bags.
light teal bags contain 1 pale olive bag.
posh fuchsia bags contain 5 bright blue bags, 2 dotted yellow bags, 4 wavy coral bags.
striped violet bags contain 5 wavy cyan bags, 1 faded lavender bag, 4 shiny silver bags, 2 striped lavender bags.
plaid crimson bags contain 5 dull chartreuse bags, 2 dark orange bags, 4 pale black bags, 2 light purple bags.
light olive bags contain 4 dull turquoise bags, 5 dark purple bags, 4 muted chartreuse bags, 3 dark teal bags.
dim magenta bags contain 5 posh gray bags, 5 vibrant fuchsia bags, 1 posh chartreuse bag.
striped aqua bags contain 1 pale violet bag, 3 drab lime bags, 1 dark beige bag, 3 light brown bags.
dotted white bags contain 1 dark gray bag, 1 vibrant orange bag, 5 muted bronze bags, 5 posh gray bags.
faded black bags contain 1 shiny purple bag, 2 mirrored blue bags, 5 vibrant coral bags, 5 shiny turquoise bags.
dotted black bags contain 3 drab green bags, 4 plaid beige bags.
dotted gold bags contain 2 dark bronze bags, 1 drab fuchsia bag.
dark tomato bags contain 4 dotted plum bags, 4 mirrored crimson bags.
shiny tan bags contain 2 pale brown bags.
muted gold bags contain 1 light indigo bag.
dim gold bags contain 5 light salmon bags.
dull yellow bags contain 2 striped violet bags.
bright white bags contain 1 pale black bag.
light purple bags contain 1 faded salmon bag, 5 dim bronze bags, 3 shiny gray bags, 5 dull teal bags.
shiny magenta bags contain 5 vibrant blue bags, 4 muted crimson bags, 4 faded white bags.
faded brown bags contain 2 dotted plum bags, 1 dotted salmon bag.
posh coral bags contain 5 dark gray bags.
dim green bags contain 1 light turquoise bag, 2 dark aqua bags, 4 drab magenta bags, 2 faded maroon bags.
dull red bags contain 5 faded red bags, 3 drab salmon bags, 1 faded blue bag.
clear plum bags contain 2 dotted tan bags, 3 light blue bags, 3 clear magenta bags, 2 drab green bags.
mirrored lavender bags contain 1 vibrant purple bag, 1 vibrant plum bag, 2 dark teal bags.
dim salmon bags contain 5 drab fuchsia bags, 1 drab blue bag.
plaid maroon bags contain 1 clear violet bag.
dim fuchsia bags contain 5 dim gold bags, 4 mirrored indigo bags.
dull olive bags contain 4 faded gray bags, 5 shiny bronze bags.
muted brown bags contain 1 vibrant coral bag, 3 dark black bags, 4 dotted red bags.
muted lavender bags contain 3 dim aqua bags, 5 wavy tomato bags.
faded lime bags contain 4 dim chartreuse bags, 5 drab beige bags.
muted yellow bags contain 3 dark white bags.
dark purple bags contain 3 dotted teal bags, 1 wavy tomato bag.
light crimson bags contain 1 muted cyan bag, 1 pale coral bag.
muted green bags contain 2 faded plum bags, 2 light chartreuse bags, 4 dull chartreuse bags, 4 vibrant turquoise bags.
vibrant beige bags contain 3 striped green bags, 1 wavy gold bag, 1 mirrored chartreuse bag.
shiny tomato bags contain 1 posh bronze bag, 4 pale salmon bags, 4 vibrant orange bags, 1 faded aqua bag.
bright yellow bags contain 2 dull lavender bags, 3 plaid purple bags, 4 light beige bags, 5 clear indigo bags.
clear black bags contain 4 dark plum bags.
posh brown bags contain 5 plaid fuchsia bags, 1 clear turquoise bag, 5 drab white bags.
shiny lime bags contain 1 light beige bag.
mirrored blue bags contain 4 drab salmon bags, 4 dim indigo bags.
dull salmon bags contain 3 drab white bags, 2 vibrant orange bags.
plaid teal bags contain no other bags.
plaid blue bags contain 1 dull indigo bag, 4 wavy black bags, 4 clear red bags.
"""

test_input = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

test_input2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""

bags = {}
reverse_bags = {}
for line in input.splitlines():
    result = re.fullmatch(r"(.+) bags contain (.+)\.", line)
    result = result.groups()

    outer = result[0]
    if result[1] == "no other bags":
        continue

    parts = result[1].split(",")
    inner = []
    for part in parts:
        result = re.fullmatch(r" *([0-9]+) ([^,\.]+) bags?", part)
        result = result.groups()

        inner.append((result[0], result[1]))
        if result[1] not in reverse_bags:
            reverse_bags[result[1]] = []
        reverse_bags[result[1]].append((result[0], outer))
    bags[outer] = inner

import pprint
pprint.pprint(bags)
print("")
pprint.pprint(reverse_bags)

can_contain = {}

def traverse(bags, name):
    total = 0
    can_contain[name] = True
    if name not in bags:
        return 0
    print("Visiting", name)
    for item in bags[name]:
        children = traverse(bags, item[1]) + 1
        total += int(item[0]) * children
    return total

total = traverse(bags, 'shiny gold')

print(len(can_contain) - 1)
print(total)
