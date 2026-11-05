# Part 3 — What "Learning" Actually Means

*[← Part 2](ai-internals-02-the-perceptron.md) · [Series index](ai-internals-00-index.md) · [Glossary](ai-internals-glossary.md) · Next: [Backpropagation →](ai-internals-04-backpropagation.md)*

Every AI model starts out with random numbers. It gets better by making mistakes over and over, each time getting a little closer to the right answer.

In Part 2, we looked at a neuron choosing colleges, with its knowledge stored in its weights, or the knobs from Part 1b. But where do those numbers come from?

If you tried the [**Pick a College**](playground.html#college) game, you have already seen this happen. You chose to apply or skip for each college, pressed learn, and the knobs changed on their own. When the neuron matches your choice, nothing happens. If it disagrees, each knob gets a small push in the right direction. This is Rosenblatt's rule from 1958.

But that rule only tells if the neuron made a mistake, not how big the mistake was. Both small and large errors get the same adjustment. Modern training does better than this, and you have probably done something similar when cooking.

## Learning is chasing the perfect dish

In Part 1b, we used a recipe as an example of a function: you put in ingredients and get dinner. Now, think about making a new dish. You taste it and notice something is not quite right. Maybe it is too salty or needs more pepper. You make a small change, taste again, and keep adjusting. A little too much salt is not a big problem, but a lot can ruin the meal.

That is what learning looks like. The ingredients stay the same, but the amounts you use change, just like the knobs. Training repeats three steps, all using one setting:

1. **Taste the dish** and see how far off you are.
2. **Figure out what to change** for each ingredient. Should you add more salt or less, and how much would it help?
3. **Adjust each ingredient** by its own amount, then taste again.

The **step size** (learning rate) controls how big each change is, from pinches to handfuls.

There is no "aha" moment. It is more like sanding wood than thinking.

Let's go through the steps one by one, using the college neuron from Part 2.

## Step 1: You cannot improve what you cannot measure

"It tastes off" is not a measurement. Saying "it scores 4 out of 10" gives you a number to improve. Rosenblatt's rule only says "it tastes off": just right or wrong, nothing else. That is a yes-or-no grade. Training needs to know how confident the neuron was, not just if it was correct.

So the neuron needs to show how confident it is. Instead of just saying "apply," it might say, "I am 20% sure you would apply to Pine Ridge Tech." In Part 2, the neuron added up a total before making a decision. Now, instead of a simple switch, we use that total to show confidence. If the total is much higher than the bar, it is very sure, close to 100%. If it is much lower, it is close to 0%. Right at the bar is 50%, like flipping a coin. Part 7 explains this in detail.

Now we can give it a grade. Look at the answer you chose and see how confident the neuron was. If it was very sure of your answer, the penalty is small. If it was not sure at all, the penalty is large. This grade is called the **loss**: it is a single number, big when the model is wrong and zero when it is perfect. Here, "wrong" means different from your answer, not necessarily wrong about the world. From now on, the goal is to make that number smaller.

The most common type of loss is called **cross-entropy**. The name sounds more complicated than it really is:

<!-- latex: \text{loss} = -\log\left(\text{the probability the model gave to the correct answer}\right) -->
```
loss = −log(the probability the model gave to the correct answer)
```

The `log` sets the grading scale. It makes the penalty increase quickly as the percentage gets closer to zero. Here is what that looks like:

| How sure the model was of the right answer | Loss |
|---|---|
| 100%, certain and correct | **0**, nothing to fix |
| 50%, a coin toss | **0.7** |
| 5%, mostly wrong | **3.0** |
| 0.1%, sure of the wrong answer | **6.9** |

Let’s go back to the colleges. You chose to apply to Pine Ridge Tech, but the neuron was only 20% sure. That gives a loss of about 1.6, which is not great but not terrible. You chose to skip Lakeview College, but the neuron was 99.9% sure you would apply. That means it was only 0.1% sure of your real answer, so the loss is 6.9. Rosenblatt's rule treats both cases the same, but cross-entropy says the second is more than four times worse. Being wrong is bad, but being very confident and wrong is even worse, like a cook who thought it was salt but used sugar.

This grading also applies to the trophy sentence from Part 1b: *"The trophy didn't fit in the case because it was too..."*. If the model was 41% sure the answer was "big," and "big" is correct, the loss is about 0.9.

The loss tells you the dish turned out badly, but it does not say if salt, pepper, or heat was the problem. That is what step 2 is for.

## Step 2: Find which way is downhill

Imagine the loss as a landscape. Each setting of the ten college knobs is a point on the map, and the height at that point is the loss. High ground means the model is very wrong, and the valley floor is as correct as possible. Training starts at a random spot and moves down the slope.

But the model cannot see the whole valley. Imagine pouring water on a mountainside. The water only feels the slope where it is and flows that way. Training works the same way.

<figure style="margin:0 0 18px">
<svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg" role="img" style="max-width:100%;height:auto" aria-label="A loss curve shaped like a valley. A ball starts high on the left; the green tangent line shows the slope there. Real gradient-descent steps follow, each shorter than the last as the ground flattens, ending near the bottom of the valley.">
  <style>
    .gd-ground{fill:var(--panel2,#1c2230);}
    .gd-curve{fill:none;stroke:var(--dim,#9aa7b8);stroke-width:2.25;stroke-linejoin:round;}
    .gd-axis{stroke:var(--line,#2b3444);stroke-width:1.25;}
    .gd-grid{stroke:var(--line,#2b3444);stroke-width:1;stroke-dasharray:2 4;}
    .gd-lbl{fill:var(--ink,#e6edf3);font:600 12.5px var(--sans,system-ui,-apple-system,'Segoe UI',sans-serif);}
    .gd-sub{fill:var(--dim,#9aa7b8);font:12px var(--sans,system-ui,-apple-system,'Segoe UI',sans-serif);}
    .gd-ax{fill:var(--dim,#9aa7b8);font:11.5px var(--sans,system-ui,-apple-system,'Segoe UI',sans-serif);letter-spacing:.02em;}
    .gd-num{fill:var(--dim,#9aa7b8);font:600 10.5px var(--mono,ui-monospace,monospace);}
    .gd-lead{stroke:var(--dim,#9aa7b8);stroke-width:1;fill:none;}
    .gd-blue{fill:var(--accent,#4c8dff);}
    .gd-blueS{stroke:var(--accent,#4c8dff);stroke-width:1.75;fill:none;}
    .gd-amber{fill:#cf7a12;}
    .gd-amberS{stroke:#cf7a12;stroke-width:2;fill:none;stroke-dasharray:5 4;}
    .gd-water{fill:#2491c9;fill-opacity:.55;}
    .gd-surf{stroke:#2491c9;stroke-width:2;}
    .gd-tan{stroke:#17946a;stroke-width:2.5;stroke-linecap:round;}
    .gd-tanT{fill:var(--ink,#e6edf3);font:600 12.5px var(--sans,system-ui,-apple-system,'Segoe UI',sans-serif);}
    .gd-halo{stroke:var(--bg,#0d1117);stroke-width:4;paint-order:stroke;stroke-linejoin:round;}
  </style>
  <defs><marker id="gd-ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--accent,#4c8dff)"/></marker></defs>
  <line class="gd-grid" x1="78" y1="80" x2="696" y2="80"/>
  <line class="gd-grid" x1="78" y1="138" x2="696" y2="138"/>
  <line class="gd-grid" x1="78" y1="196" x2="696" y2="196"/>
  <line class="gd-axis" x1="78" y1="254" x2="696" y2="254"/>
  <line class="gd-axis" x1="78" y1="22" x2="78" y2="254"/>
  <text class="gd-ax" x="66" y="26" text-anchor="end">high</text>
  <text class="gd-ax" x="66" y="254" text-anchor="end">low</text>
  <text class="gd-ax" x="50" y="138" text-anchor="middle" transform="rotate(-90 50,138)">loss (how wrong)</text>
  <text class="gd-ax" x="387.0" y="278" text-anchor="middle">the setting of one knob, say cost</text>
  <path class="gd-ground" d="M78,34.1 L80.6,37.3 L83.2,40.4 L85.7,43.6 L88.3,46.7 L90.9,49.8 L93.4,52.9 L96,55.9 L98.6,58.9 L101.2,61.9 L103.8,64.9 L106.3,67.8 L108.9,70.7 L111.5,73.6 L114,76.4 L116.6,79.2 L119.2,82 L121.8,84.8 L124.3,87.6 L126.9,90.3 L129.5,93 L132.1,95.6 L134.7,98.3 L137.2,100.9 L139.8,103.5 L142.4,106 L144.9,108.6 L147.5,111.1 L150.1,113.5 L152.7,116 L155.2,118.4 L157.8,120.8 L160.4,123.2 L163,125.5 L165.6,127.8 L168.1,130.1 L170.7,132.4 L173.3,134.6 L175.8,136.8 L178.4,139 L181,141.2 L183.6,143.3 L186.1,145.4 L188.7,147.5 L191.3,149.5 L193.9,151.6 L196.4,153.6 L199,155.5 L201.6,157.5 L204.2,159.4 L206.8,161.3 L209.3,163.1 L211.9,165 L214.5,166.8 L217.1,168.6 L219.6,170.3 L222.2,172 L224.8,173.7 L227.3,175.4 L229.9,177.1 L232.5,178.7 L235.1,180.3 L237.7,181.8 L240.2,183.4 L242.8,184.9 L245.4,186.4 L248,187.8 L250.5,189.3 L253.1,190.7 L255.7,192.1 L258.2,193.4 L260.8,194.7 L263.4,196 L266,197.3 L268.6,198.5 L271.1,199.8 L273.7,201 L276.3,202.1 L278.9,203.3 L281.4,204.4 L284,205.5 L286.6,206.5 L289.1,207.5 L291.7,208.6 L294.3,209.5 L296.9,210.5 L299.4,211.4 L302,212.3 L304.6,213.2 L307.2,214 L309.8,214.8 L312.3,215.6 L314.9,216.4 L317.5,217.1 L320.1,217.8 L322.6,218.5 L325.2,219.2 L327.8,219.8 L330.4,220.4 L332.9,221 L335.5,221.5 L338.1,222 L340.6,222.5 L343.2,223 L345.8,223.5 L348.4,223.9 L350.9,224.3 L353.5,224.6 L356.1,225 L358.7,225.3 L361.2,225.5 L363.8,225.8 L366.4,226 L369,226.2 L371.6,226.4 L374.1,226.5 L376.7,226.7 L379.3,226.8 L381.8,226.8 L384.4,226.9 L387,226.9 L389.6,226.9 L392.1,226.8 L394.7,226.8 L397.3,226.7 L399.9,226.5 L402.4,226.4 L405,226.2 L407.6,226 L410.2,225.8 L412.8,225.5 L415.3,225.3 L417.9,225 L420.5,224.6 L423.1,224.3 L425.6,223.9 L428.2,223.5 L430.8,223 L433.3,222.5 L435.9,222 L438.5,221.5 L441.1,221 L443.6,220.4 L446.2,219.8 L448.8,219.2 L451.4,218.5 L453.9,217.8 L456.5,217.1 L459.1,216.4 L461.7,215.6 L464.2,214.8 L466.8,214 L469.4,213.2 L472,212.3 L474.6,211.4 L477.1,210.5 L479.7,209.5 L482.3,208.6 L484.9,207.5 L487.4,206.5 L490,205.5 L492.6,204.4 L495.2,203.3 L497.7,202.1 L500.3,201 L502.9,199.8 L505.4,198.5 L508,197.3 L510.6,196 L513.2,194.7 L515.8,193.4 L518.3,192.1 L520.9,190.7 L523.5,189.3 L526,187.8 L528.6,186.4 L531.2,184.9 L533.8,183.4 L536.4,181.8 L538.9,180.3 L541.5,178.7 L544.1,177.1 L546.6,175.4 L549.2,173.7 L551.8,172 L554.4,170.3 L557,168.6 L559.5,166.8 L562.1,165 L564.7,163.1 L567.2,161.3 L569.8,159.4 L572.4,157.5 L575,155.5 L577.5,153.6 L580.1,151.6 L582.7,149.5 L585.3,147.5 L587.8,145.4 L590.4,143.3 L593,141.2 L595.6,139 L598.1,136.8 L600.7,134.6 L603.3,132.4 L605.9,130.1 L608.4,127.8 L611,125.5 L613.6,123.2 L616.2,120.8 L618.8,118.4 L621.3,116 L623.9,113.5 L626.5,111.1 L629.1,108.6 L631.6,106 L634.2,103.5 L636.8,100.9 L639.4,98.3 L641.9,95.6 L644.5,93 L647.1,90.3 L649.6,87.6 L652.2,84.8 L654.8,82 L657.4,79.2 L660,76.4 L662.5,73.6 L665.1,70.7 L667.7,67.8 L670.2,64.9 L672.8,61.9 L675.4,58.9 L678,55.9 L680.5,52.9 L683.1,49.8 L685.7,46.7 L688.3,43.6 L690.9,40.4 L693.4,37.3 L696,34.1 L696,254 L78,254 Z"/>
  <path class="gd-curve" d="M78,34.1 L80.6,37.3 L83.2,40.4 L85.7,43.6 L88.3,46.7 L90.9,49.8 L93.4,52.9 L96,55.9 L98.6,58.9 L101.2,61.9 L103.8,64.9 L106.3,67.8 L108.9,70.7 L111.5,73.6 L114,76.4 L116.6,79.2 L119.2,82 L121.8,84.8 L124.3,87.6 L126.9,90.3 L129.5,93 L132.1,95.6 L134.7,98.3 L137.2,100.9 L139.8,103.5 L142.4,106 L144.9,108.6 L147.5,111.1 L150.1,113.5 L152.7,116 L155.2,118.4 L157.8,120.8 L160.4,123.2 L163,125.5 L165.6,127.8 L168.1,130.1 L170.7,132.4 L173.3,134.6 L175.8,136.8 L178.4,139 L181,141.2 L183.6,143.3 L186.1,145.4 L188.7,147.5 L191.3,149.5 L193.9,151.6 L196.4,153.6 L199,155.5 L201.6,157.5 L204.2,159.4 L206.8,161.3 L209.3,163.1 L211.9,165 L214.5,166.8 L217.1,168.6 L219.6,170.3 L222.2,172 L224.8,173.7 L227.3,175.4 L229.9,177.1 L232.5,178.7 L235.1,180.3 L237.7,181.8 L240.2,183.4 L242.8,184.9 L245.4,186.4 L248,187.8 L250.5,189.3 L253.1,190.7 L255.7,192.1 L258.2,193.4 L260.8,194.7 L263.4,196 L266,197.3 L268.6,198.5 L271.1,199.8 L273.7,201 L276.3,202.1 L278.9,203.3 L281.4,204.4 L284,205.5 L286.6,206.5 L289.1,207.5 L291.7,208.6 L294.3,209.5 L296.9,210.5 L299.4,211.4 L302,212.3 L304.6,213.2 L307.2,214 L309.8,214.8 L312.3,215.6 L314.9,216.4 L317.5,217.1 L320.1,217.8 L322.6,218.5 L325.2,219.2 L327.8,219.8 L330.4,220.4 L332.9,221 L335.5,221.5 L338.1,222 L340.6,222.5 L343.2,223 L345.8,223.5 L348.4,223.9 L350.9,224.3 L353.5,224.6 L356.1,225 L358.7,225.3 L361.2,225.5 L363.8,225.8 L366.4,226 L369,226.2 L371.6,226.4 L374.1,226.5 L376.7,226.7 L379.3,226.8 L381.8,226.8 L384.4,226.9 L387,226.9 L389.6,226.9 L392.1,226.8 L394.7,226.8 L397.3,226.7 L399.9,226.5 L402.4,226.4 L405,226.2 L407.6,226 L410.2,225.8 L412.8,225.5 L415.3,225.3 L417.9,225 L420.5,224.6 L423.1,224.3 L425.6,223.9 L428.2,223.5 L430.8,223 L433.3,222.5 L435.9,222 L438.5,221.5 L441.1,221 L443.6,220.4 L446.2,219.8 L448.8,219.2 L451.4,218.5 L453.9,217.8 L456.5,217.1 L459.1,216.4 L461.7,215.6 L464.2,214.8 L466.8,214 L469.4,213.2 L472,212.3 L474.6,211.4 L477.1,210.5 L479.7,209.5 L482.3,208.6 L484.9,207.5 L487.4,206.5 L490,205.5 L492.6,204.4 L495.2,203.3 L497.7,202.1 L500.3,201 L502.9,199.8 L505.4,198.5 L508,197.3 L510.6,196 L513.2,194.7 L515.8,193.4 L518.3,192.1 L520.9,190.7 L523.5,189.3 L526,187.8 L528.6,186.4 L531.2,184.9 L533.8,183.4 L536.4,181.8 L538.9,180.3 L541.5,178.7 L544.1,177.1 L546.6,175.4 L549.2,173.7 L551.8,172 L554.4,170.3 L557,168.6 L559.5,166.8 L562.1,165 L564.7,163.1 L567.2,161.3 L569.8,159.4 L572.4,157.5 L575,155.5 L577.5,153.6 L580.1,151.6 L582.7,149.5 L585.3,147.5 L587.8,145.4 L590.4,143.3 L593,141.2 L595.6,139 L598.1,136.8 L600.7,134.6 L603.3,132.4 L605.9,130.1 L608.4,127.8 L611,125.5 L613.6,123.2 L616.2,120.8 L618.8,118.4 L621.3,116 L623.9,113.5 L626.5,111.1 L629.1,108.6 L631.6,106 L634.2,103.5 L636.8,100.9 L639.4,98.3 L641.9,95.6 L644.5,93 L647.1,90.3 L649.6,87.6 L652.2,84.8 L654.8,82 L657.4,79.2 L660,76.4 L662.5,73.6 L665.1,70.7 L667.7,67.8 L670.2,64.9 L672.8,61.9 L675.4,58.9 L678,55.9 L680.5,52.9 L683.1,49.8 L685.7,46.7 L688.3,43.6 L690.9,40.4 L693.4,37.3 L696,34.1"/>
  <line class="gd-tan" x1="91.9" y1="53.1" x2="156.8" y2="122"/>
  <line class="gd-blueS" x1="129.6" y1="83.2" x2="213.6" y2="156.2" marker-end="url(#gd-ah)"/>
  <line class="gd-blueS" x1="225" y1="164.2" x2="273.3" y2="191.1" marker-end="url(#gd-ah)"/>
  <line class="gd-blueS" x1="286" y1="196.9" x2="311.6" y2="206" marker-end="url(#gd-ah)"/>
  <line class="gd-blueS" x1="325" y1="209.9" x2="336.1" y2="212.4"/>
  <line class="gd-blueS" x1="349.9" y1="215" x2="351.9" y2="215.3"/>
  <circle class="gd-blue" cx="124.3" cy="87.6" r="6.5"/>
  <circle class="gd-blue" cx="218.9" cy="169.8" r="4.5"/>
  <circle class="gd-blue" cx="279.4" cy="203.5" r="4.5"/>
  <circle class="gd-blue" cx="318.1" cy="217.3" r="4.5"/>
  <circle class="gd-blue" cx="342.9" cy="223" r="4.5"/>
  <circle class="gd-blue" cx="358.8" cy="225.3" r="4.5"/>
  <text class="gd-lbl" x="140.3" y="73.6">start: random knobs</text>
  <path class="gd-lead" d="M139.8,112.2 L126,142.1"/>
  <text class="gd-tanT" x="88" y="156.1">the slope here</text>
  <text class="gd-tanT" x="88" y="172.1">is the gradient</text>
  <text class="gd-sub" x="202.9" y="213.8" text-anchor="end">steep ground: big steps</text>
  <text class="gd-sub" x="387" y="148.5" text-anchor="middle">flatter ground: smaller steps</text>
  <path class="gd-lead" d="M387,156.5 L342.9,209"/>
  <text class="gd-lbl" x="387" y="250.9" text-anchor="middle">the valley: lowest loss</text>
</svg>
<figcaption style="font-size:13px;color:var(--dim,#9aa7b8);margin-top:6px">In real gradient descent with one knob, the steps get smaller on their own as the ground becomes flatter.</figcaption>
</figure>

To sense the slope, training asks each knob one question:

**If I turn this knob just a little, does the loss improve or get worse, and by how much?**

Take the cost knob as an example. Turn it up a bit. Does the neuron become more confident you would apply to Pine Ridge Tech? Does it become less sure about Lakeview? Add up these changes for every college you considered, and you get the answer for cost. Then do the same for distance, program, weather, and the other factors.

This answer is called the **gradient**. It tells you the direction and steepness for each knob. Every knob has its own gradient.

Think about the shape of the valley, like with the salt example. Far from the bottom, the ground is steep, so a small change makes a big difference. Near the bottom, the ground is flat, so a little more or less does not matter much.

This is also why we use a percentage instead of a switch. If you turn a knob just a little, a switch usually does not change, so the loss stays the same and you cannot tell which way to go. With a percentage, every small change affects the output a bit, so there is almost always a slope to follow.

## Step 3: Adjust everything, then taste again

Now move all the knobs down the slope at the same time. How far each knob moves depends on its own slope, adjusted by a shared step size. Steep slopes mean bigger moves, and flat slopes mean smaller ones. That is why Lakeview's loss can be four times Pine Ridge's, but its adjustment is not four times bigger. The loss tells you how bad things are, while the slope tells you what to change.

Then measure again, find the new slope, and adjust again. There is no hidden extra step. Even the biggest models in the world are trained using advanced versions of this basic loop.

## The Goldilocks problem: how big should each step be?

The shared step size is called the **learning rate**. It does not replace the slope; it just scales it. Each knob moves by its slope multiplied by the learning rate. Getting this setting right can take a lot of time.

If the learning rate is too small, it is like adding salt one grain at a time. You will get there eventually, but it takes a very long time.

If the learning rate is too large, you might throw in a handful of salt, find it too salty, add water, and end up with a bland dish. The neuron does something similar: it might go from ignoring cost to focusing only on cost, then swing back past where it started. Each swing gets bigger until the loss becomes `NaN`, which stands for "not a number". That is the computer's way of giving up. I spent hours in graduate school adjusting this setting and running experiments. It did not feel like math; it felt more like tuning a carburetor.

> ⛷️ **Try it out:** In the playground, [**Downhill**](playground.html#downhill) lets you see this process with two knobs. Drag the ball, then increase the learning rate. Around 0.22, the ball flies off the screen. Each frame is calculated in real time, so you are watching the math break down.

## Can the water get stuck?

Let’s return to the water on the mountain.

<figure style="margin:0 0 18px">
<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" role="img" style="max-width:100%;height:auto" aria-label="A loss landscape with a small hollow high on the left and a deeper valley on the right. Two real gradient-descent runs start at the same point. Small steps creep down into the hollow and stop there, in a lake: a local minimum. Big steps leap over the rim on the very first step and roll on down to the global minimum.">
  <style>
    .lk-ground{fill:var(--panel2,#1c2230);}
    .lk-curve{fill:none;stroke:var(--dim,#9aa7b8);stroke-width:2.25;stroke-linejoin:round;}
    .lk-axis{stroke:var(--line,#2b3444);stroke-width:1.25;}
    .lk-grid{stroke:var(--line,#2b3444);stroke-width:1;stroke-dasharray:2 4;}
    .lk-lbl{fill:var(--ink,#e6edf3);font:600 12.5px var(--sans,system-ui,-apple-system,'Segoe UI',sans-serif);}
    .lk-sub{fill:var(--dim,#9aa7b8);font:12px var(--sans,system-ui,-apple-system,'Segoe UI',sans-serif);}
    .lk-ax{fill:var(--dim,#9aa7b8);font:11.5px var(--sans,system-ui,-apple-system,'Segoe UI',sans-serif);letter-spacing:.02em;}
    .lk-num{fill:var(--dim,#9aa7b8);font:600 10.5px var(--mono,ui-monospace,monospace);}
    .lk-lead{stroke:var(--dim,#9aa7b8);stroke-width:1;fill:none;}
    .lk-blue{fill:var(--accent,#4c8dff);}
    .lk-blueS{stroke:var(--accent,#4c8dff);stroke-width:1.75;fill:none;}
    .lk-amber{fill:#cf7a12;}
    .lk-amberS{stroke:#cf7a12;stroke-width:2;fill:none;stroke-dasharray:5 4;}
    .lk-water{fill:#2491c9;fill-opacity:.55;}
    .lk-surf{stroke:#2491c9;stroke-width:2;}
    .lk-tan{stroke:#17946a;stroke-width:2.5;stroke-linecap:round;}
    .lk-tanT{fill:var(--ink,#e6edf3);font:600 12.5px var(--sans,system-ui,-apple-system,'Segoe UI',sans-serif);}
    .lk-halo{stroke:var(--bg,#0d1117);stroke-width:4;paint-order:stroke;stroke-linejoin:round;}
  </style>
  <defs><marker id="lk-ahB" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#cf7a12"/></marker></defs>
  <line class="lk-grid" x1="78" y1="146.5" x2="696" y2="146.5"/>
  <line class="lk-grid" x1="78" y1="209" x2="696" y2="209"/>
  <line class="lk-grid" x1="78" y1="271.5" x2="696" y2="271.5"/>
  <line class="lk-axis" x1="78" y1="334" x2="696" y2="334"/>
  <line class="lk-axis" x1="78" y1="84" x2="78" y2="334"/>
  <text class="lk-ax" x="66" y="88" text-anchor="end">high</text>
  <text class="lk-ax" x="66" y="334" text-anchor="end">low</text>
  <text class="lk-ax" x="50" y="209" text-anchor="middle" transform="rotate(-90 50,209)">loss (how wrong)</text>
  <text class="lk-ax" x="387.0" y="358" text-anchor="middle">the setting of the knobs</text>
  <path class="lk-ground" d="M78,90.8 L80.6,98.4 L83.1,105.8 L85.7,112.9 L88.3,119.8 L90.9,126.4 L93.4,132.8 L96,139 L98.6,144.9 L101.2,150.6 L103.8,156.1 L106.3,161.4 L108.9,166.5 L111.5,171.3 L114.1,176 L116.6,180.4 L119.2,184.7 L121.8,188.7 L124.4,192.6 L126.9,196.3 L129.5,199.9 L132.1,203.2 L134.7,206.4 L137.2,209.5 L139.8,212.3 L142.4,215 L144.9,217.6 L147.5,220 L150.1,222.3 L152.7,224.4 L155.2,226.4 L157.8,228.3 L160.4,230 L163,231.6 L165.5,233.1 L168.1,234.5 L170.7,235.8 L173.3,236.9 L175.9,238 L178.4,238.9 L181,239.8 L183.6,240.5 L186.1,241.2 L188.7,241.8 L191.3,242.2 L193.9,242.6 L196.4,243 L199,243.2 L201.6,243.4 L204.2,243.5 L206.8,243.5 L209.3,243.5 L211.9,243.4 L214.5,243.2 L217,243 L219.6,242.8 L222.2,242.5 L224.8,242.1 L227.3,241.7 L229.9,241.3 L232.5,240.8 L235.1,240.3 L237.6,239.7 L240.2,239.1 L242.8,238.5 L245.4,237.9 L247.9,237.2 L250.5,236.5 L253.1,235.8 L255.7,235.1 L258.2,234.4 L260.8,233.6 L263.4,232.9 L266,232.1 L268.5,231.3 L271.1,230.5 L273.7,229.8 L276.3,229 L278.8,228.2 L281.4,227.4 L284,226.6 L286.6,225.9 L289.1,225.1 L291.7,224.3 L294.3,223.6 L296.9,222.9 L299.5,222.2 L302,221.5 L304.6,220.8 L307.2,220.1 L309.8,219.5 L312.3,218.8 L314.9,218.2 L317.5,217.7 L320.1,217.1 L322.6,216.6 L325.2,216.1 L327.8,215.6 L330.4,215.2 L332.9,214.8 L335.5,214.4 L338.1,214.1 L340.6,213.8 L343.2,213.5 L345.8,213.2 L348.4,213 L350.9,212.9 L353.5,212.7 L356.1,212.7 L358.7,212.6 L361.2,212.6 L363.8,212.6 L366.4,212.7 L369,212.8 L371.6,212.9 L374.1,213.1 L376.7,213.3 L379.3,213.6 L381.9,213.9 L384.4,214.3 L387,214.7 L389.6,215.1 L392.1,215.6 L394.7,216.1 L397.3,216.7 L399.9,217.3 L402.4,217.9 L405,218.6 L407.6,219.4 L410.2,220.2 L412.8,221 L415.3,221.8 L417.9,222.7 L420.5,223.7 L423.1,224.7 L425.6,225.7 L428.2,226.7 L430.8,227.8 L433.3,229 L435.9,230.1 L438.5,231.4 L441.1,232.6 L443.6,233.9 L446.2,235.2 L448.8,236.5 L451.4,237.9 L453.9,239.3 L456.5,240.8 L459.1,242.3 L461.7,243.8 L464.2,245.3 L466.8,246.8 L469.4,248.4 L472,250 L474.6,251.6 L477.1,253.3 L479.7,255 L482.3,256.6 L484.9,258.4 L487.4,260.1 L490,261.8 L492.6,263.6 L495.2,265.3 L497.7,267.1 L500.3,268.9 L502.9,270.6 L505.4,272.4 L508,274.2 L510.6,276 L513.2,277.8 L515.8,279.6 L518.3,281.3 L520.9,283.1 L523.5,284.9 L526,286.6 L528.6,288.4 L531.2,290.1 L533.8,291.8 L536.4,293.5 L538.9,295.2 L541.5,296.8 L544.1,298.4 L546.7,300 L549.2,301.5 L551.8,303.1 L554.4,304.5 L557,306 L559.5,307.4 L562.1,308.7 L564.7,310 L567.2,311.3 L569.8,312.5 L572.4,313.7 L575,314.7 L577.5,315.8 L580.1,316.7 L582.7,317.6 L585.3,318.5 L587.8,319.2 L590.4,319.9 L593,320.5 L595.6,321 L598.1,321.4 L600.7,321.8 L603.3,322 L605.9,322.2 L608.4,322.2 L611,322.2 L613.6,322 L616.2,321.7 L618.8,321.4 L621.3,320.9 L623.9,320.2 L626.5,319.5 L629,318.6 L631.6,317.6 L634.2,316.5 L636.8,315.2 L639.4,313.8 L641.9,312.2 L644.5,310.5 L647.1,308.6 L649.6,306.6 L652.2,304.4 L654.8,302 L657.4,299.5 L660,296.8 L662.5,293.9 L665.1,290.8 L667.7,287.5 L670.2,284 L672.8,280.4 L675.4,276.5 L678,272.5 L680.5,268.2 L683.1,263.7 L685.7,259 L688.3,254 L690.9,248.8 L693.4,243.4 L696,237.8 L696,334 L78,334 Z"/>
  <path class="lk-curve" d="M78,90.8 L80.6,98.4 L83.1,105.8 L85.7,112.9 L88.3,119.8 L90.9,126.4 L93.4,132.8 L96,139 L98.6,144.9 L101.2,150.6 L103.8,156.1 L106.3,161.4 L108.9,166.5 L111.5,171.3 L114.1,176 L116.6,180.4 L119.2,184.7 L121.8,188.7 L124.4,192.6 L126.9,196.3 L129.5,199.9 L132.1,203.2 L134.7,206.4 L137.2,209.5 L139.8,212.3 L142.4,215 L144.9,217.6 L147.5,220 L150.1,222.3 L152.7,224.4 L155.2,226.4 L157.8,228.3 L160.4,230 L163,231.6 L165.5,233.1 L168.1,234.5 L170.7,235.8 L173.3,236.9 L175.9,238 L178.4,238.9 L181,239.8 L183.6,240.5 L186.1,241.2 L188.7,241.8 L191.3,242.2 L193.9,242.6 L196.4,243 L199,243.2 L201.6,243.4 L204.2,243.5 L206.8,243.5 L209.3,243.5 L211.9,243.4 L214.5,243.2 L217,243 L219.6,242.8 L222.2,242.5 L224.8,242.1 L227.3,241.7 L229.9,241.3 L232.5,240.8 L235.1,240.3 L237.6,239.7 L240.2,239.1 L242.8,238.5 L245.4,237.9 L247.9,237.2 L250.5,236.5 L253.1,235.8 L255.7,235.1 L258.2,234.4 L260.8,233.6 L263.4,232.9 L266,232.1 L268.5,231.3 L271.1,230.5 L273.7,229.8 L276.3,229 L278.8,228.2 L281.4,227.4 L284,226.6 L286.6,225.9 L289.1,225.1 L291.7,224.3 L294.3,223.6 L296.9,222.9 L299.5,222.2 L302,221.5 L304.6,220.8 L307.2,220.1 L309.8,219.5 L312.3,218.8 L314.9,218.2 L317.5,217.7 L320.1,217.1 L322.6,216.6 L325.2,216.1 L327.8,215.6 L330.4,215.2 L332.9,214.8 L335.5,214.4 L338.1,214.1 L340.6,213.8 L343.2,213.5 L345.8,213.2 L348.4,213 L350.9,212.9 L353.5,212.7 L356.1,212.7 L358.7,212.6 L361.2,212.6 L363.8,212.6 L366.4,212.7 L369,212.8 L371.6,212.9 L374.1,213.1 L376.7,213.3 L379.3,213.6 L381.9,213.9 L384.4,214.3 L387,214.7 L389.6,215.1 L392.1,215.6 L394.7,216.1 L397.3,216.7 L399.9,217.3 L402.4,217.9 L405,218.6 L407.6,219.4 L410.2,220.2 L412.8,221 L415.3,221.8 L417.9,222.7 L420.5,223.7 L423.1,224.7 L425.6,225.7 L428.2,226.7 L430.8,227.8 L433.3,229 L435.9,230.1 L438.5,231.4 L441.1,232.6 L443.6,233.9 L446.2,235.2 L448.8,236.5 L451.4,237.9 L453.9,239.3 L456.5,240.8 L459.1,242.3 L461.7,243.8 L464.2,245.3 L466.8,246.8 L469.4,248.4 L472,250 L474.6,251.6 L477.1,253.3 L479.7,255 L482.3,256.6 L484.9,258.4 L487.4,260.1 L490,261.8 L492.6,263.6 L495.2,265.3 L497.7,267.1 L500.3,268.9 L502.9,270.6 L505.4,272.4 L508,274.2 L510.6,276 L513.2,277.8 L515.8,279.6 L518.3,281.3 L520.9,283.1 L523.5,284.9 L526,286.6 L528.6,288.4 L531.2,290.1 L533.8,291.8 L536.4,293.5 L538.9,295.2 L541.5,296.8 L544.1,298.4 L546.7,300 L549.2,301.5 L551.8,303.1 L554.4,304.5 L557,306 L559.5,307.4 L562.1,308.7 L564.7,310 L567.2,311.3 L569.8,312.5 L572.4,313.7 L575,314.7 L577.5,315.8 L580.1,316.7 L582.7,317.6 L585.3,318.5 L587.8,319.2 L590.4,319.9 L593,320.5 L595.6,321 L598.1,321.4 L600.7,321.8 L603.3,322 L605.9,322.2 L608.4,322.2 L611,322.2 L613.6,322 L616.2,321.7 L618.8,321.4 L621.3,320.9 L623.9,320.2 L626.5,319.5 L629,318.6 L631.6,317.6 L634.2,316.5 L636.8,315.2 L639.4,313.8 L641.9,312.2 L644.5,310.5 L647.1,308.6 L649.6,306.6 L652.2,304.4 L654.8,302 L657.4,299.5 L660,296.8 L662.5,293.9 L665.1,290.8 L667.7,287.5 L670.2,284 L672.8,280.4 L675.4,276.5 L678,272.5 L680.5,268.2 L683.1,263.7 L685.7,259 L688.3,254 L690.9,248.8 L693.4,243.4 L696,237.8"/>
  <path class="lk-water" d="M157.5,228.1 L159.6,229.5 L161.6,230.8 L163.6,232 L165.6,233.2 L167.7,234.3 L169.7,235.3 L171.7,236.3 L173.8,237.1 L175.8,238 L177.8,238.7 L179.8,239.4 L181.9,240 L183.9,240.6 L185.9,241.1 L187.9,241.6 L190,242 L192,242.4 L194,242.7 L196.1,242.9 L198.1,243.1 L200.1,243.3 L202.1,243.4 L204.2,243.5 L206.2,243.5 L208.2,243.5 L210.3,243.5 L212.3,243.4 L214.3,243.2 L216.3,243.1 L218.4,242.9 L220.4,242.7 L222.4,242.4 L224.5,242.2 L226.5,241.9 L228.5,241.5 L230.5,241.2 L232.6,240.8 L234.6,240.4 L236.6,239.9 L238.6,239.5 L240.7,239 L242.7,238.6 L244.7,238.1 L246.8,237.5 L248.8,237 L250.8,236.5 L252.8,235.9 L254.9,235.3 L256.9,234.8 L258.9,234.2 L261,233.6 L263,233 L265,232.4 L267,231.8 L269.1,231.2 L271.1,230.6 L273.1,229.9 L275.1,229.3 L277.2,228.7 L279.2,228.1 Z"/>
  <line class="lk-surf" x1="157.5" y1="228.1" x2="279.2" y2="228.1"/>
  <path class="lk-amberS" d="M88.1,111.4 Q252.3,73.4 416.4,214.2" marker-end="url(#lk-ahB)"/>
  <path class="lk-amberS" d="M416.4,214.2 Q438.1,208.2 459.9,234.7" marker-end="url(#lk-ahB)"/>
  <path class="lk-amberS" d="M459.9,234.7 Q496.1,221 532.3,282.9" marker-end="url(#lk-ahB)"/>
  <path class="lk-amberS" d="M532.3,282.9 Q573.7,266 615.1,313.9" marker-end="url(#lk-ahB)"/>
  <circle class="lk-amber" cx="416.4" cy="222.2" r="4.5"/>
  <circle class="lk-amber" cx="459.9" cy="242.7" r="4.5"/>
  <circle class="lk-amber" cx="532.3" cy="290.9" r="4.5"/>
  <circle class="lk-amber" cx="615.1" cy="321.9" r="4.5"/>
  <path class="lk-blueS" style="stroke-width:3.5" d="M88.1,119.4 L89.6,123.2 L91,126.9 L92.5,130.5 L94,134.1 L95.4,137.6 L96.9,141 L98.3,144.3 L99.8,147.6 L101.3,150.8 L102.7,153.9 L104.2,157 L105.6,160 L107.1,162.9 L108.5,165.8 L110,168.6 L111.5,171.3 L112.9,173.9 L114.4,176.5 L115.8,179.1 L117.3,181.5 L118.8,184 L120.2,186.3 L121.7,188.6 L123.1,190.8 L124.6,193 L126.1,195.1 L127.5,197.2 L129,199.2 L130.4,201.1 L131.9,203 L133.3,204.8 L134.8,206.6 L136.3,208.3 L137.7,210 L139.2,211.6 L140.6,213.2 L142.1,214.7 L143.6,216.2 L145,217.7 L146.5,219 L147.9,220.4 L149.4,221.7 L150.8,222.9 L152.3,224.1 L153.8,225.3 L155.2,226.4 L156.7,227.5 L158.1,228.5 L159.6,229.5 L161.1,230.5 L162.5,231.4 L164,232.2 L165.4,233.1 L166.9,233.9 L168.3,234.6 L169.8,235.4 L171.3,236 L172.7,236.7 L174.2,237.3 L175.6,237.9 L177.1,238.5 L178.6,239 L180,239.5 L181.5,239.9 L182.9,240.3 L184.4,240.7 L185.8,241.1 L187.3,241.4 L188.8,241.8 L190.2,242 L191.7,242.3 L193.1,242.5 L194.6,242.7 L196.1,242.9 L197.5,243.1 L199,243.2 L200.4,243.3 L201.9,243.4 L203.4,243.4 L204.8,243.5"/>
  <circle class="lk-blue" cx="153.8" cy="225.3" r="3.5"/>
  <circle class="lk-blue" cx="173.2" cy="236.9" r="3.5"/>
  <circle class="lk-blue" cx="183.9" cy="240.6" r="3.5"/>
  <circle class="lk-blue" cx="190.6" cy="242.1" r="3.5"/>
  <circle class="lk-blue" cx="195.1" cy="242.8" r="3.5"/>
  <circle class="lk-blue" cx="198.2" cy="243.1" r="3.5"/>
  <circle class="lk-blue" cx="200.5" cy="243.3" r="3.5"/>
  <circle class="lk-blue" cx="202.1" cy="243.4" r="3.5"/>
  <circle class="lk-blue" cx="203.3" cy="243.4" r="3.5"/>
  <circle class="lk-blue" cx="204.2" cy="243.5" r="3.5"/>
  <circle class="lk-blue" cx="204.8" cy="243.5" r="3.5"/>
  <circle cx="88.1" cy="119.4" r="7" fill="var(--ink,#e6edf3)"/>
  <text class="lk-lbl" x="102.1" y="123.4">start</text>
  <path class="lk-lead" d="M206.7,236.1 L206.7,300"/>
  <text class="lk-lbl" x="206.7" y="314" text-anchor="middle">trapped: a local minimum</text>
  <text class="lk-sub" x="206.7" y="328" text-anchor="middle">every way out goes uphill</text>
  <text class="lk-sub" x="360.7" y="236.6" text-anchor="middle">the rim</text>
  <path class="lk-lead" d="M612.9,310.2 L638.9,172.9"/>
  <text class="lk-lbl" x="696" y="154.9" text-anchor="end">the lowest point:</text>
  <text class="lk-lbl" x="696" y="170.9" text-anchor="end">the global minimum</text>
  <circle class="lk-blue" cx="90" cy="20" r="4.5"/>
  <text class="lk-sub" x="102" y="24">small steps, a trickle (learning rate 0.08)</text>
  <line class="lk-amberS" x1="82" y1="42" x2="98" y2="42"/>
  <text class="lk-sub" x="102" y="46">big steps, a flood (learning rate 0.40)</text>
</svg>
<figcaption style="font-size:13px;color:var(--dim,#9aa7b8);margin-top:6px">Two real runs from the same start. Only the step size differs.</figcaption>
</figure>

A slow trickle of water follows every dip. If it finds a hollow high on the mountain, it collects there because every direction out goes uphill. This hollow is called a **local minimum**: it is lower than the surrounding area, but not the lowest point, which is the **global minimum**. In the picture, a bigger step lets the water flow over the rim. That is just one example, not a solution. As the Goldilocks problem showed, a bigger step can also send you off the mountain completely.

When I was in graduate school, getting stuck in that lake was a big concern. But in large networks, it turned out to be less of a problem than we thought. With billions of knobs, the ground would have to rise in every direction to trap the water. Most flat spots are actually mountain passes, called **saddle points**: uphill in some directions, but downhill in at least one. Training can still slow down, but in practice, large networks rarely get truly stuck.

Getting the lowest possible score on the training examples was never the real goal. A model can do perfectly on the examples it trained with and still fail on new ones. What really matters is how it performs on examples it has never seen before.

> **Say this out loud:** "Training is putting a number on how wrong you are, finding which way each knob should turn to make that number smaller, and nudging every knob that way. The learning rate scales every nudge, and if it is too big, it never settles."

> **The question that takes you further:** *fine, but with a billion weights, how do you work out the gradient for every single one without doing a billion separate experiments?*

### Checkpoint

1. Rosenblatt's rule only tells you if something is right or wrong. What extra information does the cross-entropy score provide?
2. In the cooking example, what do the knobs represent, what is the loss, and what role does the learning rate play?
3. Lakeview's loss is four times higher than Pine Ridge's. Why does that not mean its adjustment is four times bigger?
4. In Part 2, the neuron ended up as a light switch. Why does this make it hard to move downhill?

*Next: [Part 4 — Backpropagation →](ai-internals-04-backpropagation.md), which answers that question and is the reason any of this is possible at all.*
