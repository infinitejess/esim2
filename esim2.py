import numpy as np
import matplotlib.pyplot as plt

'''
Input string, needs to be in the form of dose/injection date/ester
injection date is days since first injection (first injection should be at zero, you can do negatives tho)
dose in mg (obviously)
ester options are EV (valerate), EEn (enanthate), EB (benzoate), EC (cypionate), EUn (undecylate)
'''
userinput = '0/4/EV, 7/4/een, 14/2.5/een, 21/1.5/een, 28/4/ev, 35/4/een, 42/2.5/een, 49/1.5/een'

#ester a, b, c, d values (used in calculations)
een = [0.42412968, 0.43452980, 0.15291485, 333.874181]
ev = [2.38229125, 0.23345814, 1.37642769, 2596.05956]
eun = [0.29634323, 4799337.57, 0.03141554, 65.9493374]
eb = [3.22397192, 0.58870148, 70721.4018, 170500000]
ec = [0.29634323, 4799337.57, 0.03141554, 65.9493374]
#apparently ur supposed to use EEn instead of EC when ur graphing bause EC data is flawed, idk just doing what im told

'''
turns string into a properly formatted list of the following form (its like this so i can use it elsewhere easily)
[
[day of injection (counting up from start date, starting at 0), dose taken on that date, ester injected (een/ev/eu/ec)]
]
'''
injections = []
for term in [term.strip(" ()[]").lower() for term in userinput.split(',')]:
    a = term.split('/')
    a[0] = float(a[0])
    a[1] = float(a[1])
    match a[2]:
        case 'een': a[2] = een
        case 'ev': a[2] = ev
        case 'ec': a[2] = ec
        case 'eun': a[2] = eu
        case _: a[2] = een #defaults to EEn
    injections.append(a)

#sets the x limit to be a week past the last injection, you can set it to any int for a custom x axis length
xlimit = injections[(len(injections)-1)][0]+7

'''
basically the desmos calc but in python
takes the input injection list and a numpy linspace, returns the curve
i barely understand how this works but it works so thats good enough for me
'''
def total(injections, t_values):
    result = np.zeros(len(t_values))
    for i in range(len(injections)):
        for t in t_values:
            #values used in calculation, resets for each injection
            date = injections[i][0]
            dose = injections[i][1]
            a = injections[i][2][0]
            b = injections[i][2][1]
            c = injections[i][2][2]
            d = injections[i][2][3]
            #calculates the curve for each injection and adds it to the final curve
            if date < t < date + 100:
                term = (dose * d / 5) * a * b * (
                    (np.exp((-t + date) * a) / ((a - b) * (a - c))) +
                    (np.exp((-t + date) * c) / ((a - c) * (b - c))) +
                    (np.exp((-t + date) * b) * (c - a) / ((a - b) * (a - c) * (b - c)))
                )
                result[t_values == t] += term
    return result

#does stuff
t_values = np.linspace(0, 200, 1000)
y_values = total(injections, t_values)

#aesthetics
plt.rcParams.update({
    'axes.facecolor': '#1e1e1e',
    'figure.facecolor':'#1e1e1e',
    'text.color': '#d4d4d4',
    'axes.titleweight': '500',

    'xtick.color': '#1e1e1e',
    'xtick.labelcolor': '#d4d4d4',
    'ytick.color': '#1e1e1e',
    'ytick.labelcolor': '#d4d4d4',

    'grid.color': '#d4d4d4',
    'grid.linewidth': '0.1',

    'axes.spines.left': 'false',
    'axes.spines.right':'false',
    'axes.spines.top':'false',
    'axes.spines.bottom':'false',
    'font.family': 'monospace'
})

#plot curve
plt.plot(t_values, y_values, color= '#FADADD')
plt.fill_between(t_values, y_values, alpha = 0.1, color= "#FADADD", linewidth= 0)

#chart title, labels, and axis limit
plt.title('Better Injectable Estradiol Simulator')
plt.xlabel('Days')
plt.ylabel('Estradiol level (pg/mL)')
plt.grid(True)
plt.xlim(-1, xlimit)
plt.show()