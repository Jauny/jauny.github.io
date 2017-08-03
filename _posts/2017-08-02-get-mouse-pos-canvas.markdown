---
title: Get mouse position on canvas
date: 2017-08-02
layout: post
---
A simple one that I want to save here because I keep googling it and copy/pasting.

```javascript
const getMousePos = (evt, canvas) => {
  const rect = canvas.getBoundingClientRect();
  return {
    y: evt.clientY - rect.top,
    x: evt.clientX - rect.left
  }
}
```

Let's also take some time to explain what is happening here.

When a mouse event `evt` is fired, the `mouseX` and `mouseY` coordinates are recorded relative to the window (even if the mouse event is recorded from a nested DOM element[1]).

So if you want to know the position of the mouse inside your canvas, you will need to calculate the X and Y offset that the canvas has from the window's top left corner (X == 0 and Y == 0).

The DOM API offers a helper function `getBoundingClientRect` that can be called on any element, and returns a rectangle representing the surface of the element. This rectanble (a `DOMRect` object) has multiple attributes, including its X and Y offset from the window, `left` and `top`.

And using this offset, we can calculate the coordinates of the pointer relative to the current element by substracting `mouseX - rect.top` and `mouseY - rect.left`.

-------
[1] There is a new experimental specification called `offsetX` and `offsetY` which provides the offset coordinate of the mouse pointer taking into account the current DOM element's offset. Since it is still an early experimentation (only Chrome 56 at time of writing) it is not recommended to use quite now.
