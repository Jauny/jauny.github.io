---
date: 2017-08-07
layout: post
title: Physics for Asteroids
---
{% include asteroids/asteroids.html %}
_You can find the source code of the demo [here](https://github.com/jauny/asteroid)._

---

Asteroids is an old school game where you control a space vessel. In previous movements I've built, forces are constants.  
In [Snake](/snake), you either go up, down, left or right, always at the same speed.  
In [Confettis](/confettis), the introduction of gravity was interesting, but it was the only force added to the objects movements, it was constant and only impacting vertical speed.  

Here in Asteroids, you can change your vessel's direction 360 degres, and accelerating adds a force in that direction.  
Being in space, there is no gravity or friction, so a object keeps a constant speed until it is pushed by additional forces.  

Let's review how to make all of this, step by step.  


### Turn the ship around
First movement mechanics are about being able to turn.  
In Snake, press UP and the snake goes up (Y velocity becomes -1), press left and the snake goes left (X velocity becomes -1), etc.

Here, it's a little more complicated. Press left, and the ship _rotates_ left, press right and it rotates right.

To make this happen, we need to use trigonometry. Rotating implies there is a circle somewhere.  
If you start facing up, rotating 90 degres means you did 1/4 of a circle. Rotating 180 is half a circle and 360 is a full circle.  
In trigonometry, we usually use PI.  

![PI on a circle](https://tauday.com/assets/figures/pi-angles.png)

We can then use PI to set the ship's direction. Let's start with the ship facing up, which is PI/2.

Now, we need to update the ship's direction when the left and right arrows are pressed.
The ship could rotate at different speeds, and this speed will be set by the quotient used to increase/decrease the angle representing the direction.  

```javascript
var vessel = {
    dir: Math.PI/2,
    rotatingSpeed: 1,

    rotateLeft: function() {
      this.dir += this.rotatingSpeed
    },
    rotateRight: function() {
      this.dir -= this.rotatingSpeed
    }
};

console.log(vessel.dir);
=> 1.5707963267948966  // Math.PI/2

vessel.rotateRight();
console.log(vessel.dir);
=> 0.5707963267948966
```


### Move the ship
Now that we can rotate the ship's direction, we need to accelerate to move the ship. Let's clarify some terms first.  
- `speed` is the rate at which an object moves  
- `direction` is where the object is moving towards  
- Those 2 together represent the `velocity`  
- a `force` has a direction and magnitude (value at which it will impact the velocity). Force can be represented by a vector, where magnitude is its length.

When the game starts, the ship is not moving (speed = 0), it is facing up (direction = Math.PI/2) and we are not accelerating (force = 0).  

If we accelerate, the ship will gain speed toward UP (only x is changed) at a rate of 1. So accelerating only once, the speed would become 1 and the ship would start moving up 1 pixel per frame. If we accelerate again, the speed become 2 and the ship moves 2 pixels per frame.  
If we rotate the ship 90 degres, and accelerate, the ship will start moving by 1 pixel on the side.  

So this all seems pretty straight forward. But what happens if we rotate 45 degres? Or 30 degres?  
If we are not perfectly moving toward UP/DOWN/LEFT/RIGHT anymore, how do we calculate the ratio at which the acceleration impacts both x and y at the same time?  

```javascript
var vessel = {
  this.x = 200,
  this.y = 200,

  this.dir = 'UP',

  this.speedx = 0,
  this.speedy = 0,
  this.acceleration = 1,

  this.accelerate: function() {
    if (this.dir === 'UP') {
      this.speedx += this.accelerationRate;
    } else if (this.dir === 'LEFT') {
      this.speedy -= this.accelerationRate;
    } // etc...
}
```

### Sin, cos and the scary trigonometry
I promised trigonometry, so here it is. Remember sinus, cosinus, tangeant and all this (not) non-sense in high school? I remembered the terms, not what it was used for.  

Well, they are used exactly for what we need; Calculating angles so we can find the rate at which we need to update x and y.  

![sin cos tan from angle](https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Sinus_und_Kosinus_am_Einheitskreis_1.svg/418px-Sinus_und_Kosinus_am_Einheitskreis_1.svg.png)

I said previously that the `force` was a vector that had a direction and a magnitude (length).  
Our acceleration is just that: a vector with a direction (the ship's current direction) and a magnitude of 1.  

From the image above:
- the black line is the acceleration's magnitude  
- ⍬ is the ship's direction during acceleration
- the blue line is the ratio at which x is changed and is calculated from `cos(⍬)`  
- the green line is the ratio at which y is changed and is calculated from `sin(⍬)`  
- if the magnitude was bigger than 1, we'd multiply the ratios by the magnitude; `magnitude * cos(⍬)` and `magnitude * sin(⍬)`  

Example:  
```javascript
var vessel = {
    x: 200,
    y: 200,

    dir: Math.PI/3,

    speedx: 0,
    speedy: 0,

    acceleration: 1,

    accelerate: function() {
        this.speedx += this.acceleration * Math.cos(this.dir);
        this.speedy += this.acceleration * Math.sin(this.dir);
    }
};

console.log(vessel.speedx, vessel.speedy);
=> 0, 0

vessel.accelerate();
console.log(vessel.speedx, vessel.speedy);
=> 0.5, 0.86602540378445
```

There you go! Now we have a way to calculate a force and how it affects our object's velocity (speedx and speedy). Everytime we accelerate, we add the impact of this force to the existing verlocity of the ship (`this.speedx += ...` and `this.speedy = ...`) and this updates it's overall speed and direction!

{% include asteroids/asteroids-js.html %}
