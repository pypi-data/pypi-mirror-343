# the_agreement
<pre>
This is a program that simulate the difficuty of the male in China now. You can run or import the program and decoration your function.
In China, the male are facing to be a "rapist" if they have stayed with the female without the physical evidenct, just like the female_func in the program.
</pre>
## How to install?
pip:
```
pip install the_agreement
```
git:
```
git clone https://github.com/Locked-chess-official/the_agreement
```
## How to use?
<pre>
Run the code, and you need to input 1 or 2 to choose a game.
Game 1: you don't need to operation. You will known how many times you can print.
Game 2: you need to choose whether to call. If the female_func doesn't agree, you will get some punish.

Import it, and you can decoration your function.
</pre>
```
import the_agreement
@the_agreement.protection_female_wrap(0.5):
def some_function():
    ...
```
