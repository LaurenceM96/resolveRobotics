# Resolve Robotics

## First Impressions
In this readMe I'll just be laying out my thoughts as I approach the problem so you can see my working and thinking as I go along.

The first thing I notice from the outline is that the buttons do not work as expected. I'll be sorting that first, as it needs to work intuitively since its an
educational tool. I believe there should be a forward button, which moves the turtle forward in the direction it is facing, and rotation buttons so that its
direction can be changed. I might make some adjustments to this based on how it feels.<br>
Also, it needs to look like a turtle, obviously. So I'll find a turtle sprite and be implementing that.<br><br>

## Wednesday 26th
I have the buttons working as I intended, and a turtle sprite, however I need to make sure the turtle turns when you press the turn buttons.<br>
After this I want to add a programmability function, so that the user can press multiple buttons in a sequence, then press a play button and watch the turtle perform the functions they input.<br><br>

After adding some rough programmability function, I think I need to explain how it works. First the user must click "Start Programming", then they can click the inputs they wish to queue, and when they are done they can press play to see those actions happen. If the user does not click "Start Programming" the turtle functions as before; i.e. the actions happen straight away.