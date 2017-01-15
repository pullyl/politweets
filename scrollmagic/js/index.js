$(function() {

  var scrollMagicController = new ScrollMagic();
  
  // var tween0 = TweenMax.to('#animation-0', 0.3, {scale: 3});

  var tween1 = TweenMax.to('#animation-1', 2.0, {scale: 5});

  var tween2 = TweenMax.to('#animation-2', 0.4, {scale: 5,rotation: 360});


  var scene1 = new ScrollScene({triggerElement: '#scene-1',offset: 50,})
  .setClassToggle('body', 'scene-1-active')
  .setTween(tween1)
  .addTo(scrollMagicController);

  var scene2 = new ScrollScene({triggerElement: '#scene-2',offset: 50,})
  .setClassToggle('body', 'scene-2-active')
  .setTween(tween2)
  .addTo(scrollMagicController);


var tween3 = TweenMax.to('#animation-3', 0.4, {scale: 4,rotation: 360});

      var scene3 = new ScrollScene({
        triggerElement: '#scene-3',
        offset: 50
      })
      .setClassToggle('body', 'scene-3-active')
      .setTween(tween3)
      .addTo(scrollMagicController);





  // Add debug indicators fixed on right side
  scene1.addIndicators();
  scene2.addIndicators();
  scene3.addIndicators();
  
});