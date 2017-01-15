$(function() {

  var scrollMagicController = new ScrollMagic();
  
  // var tween0 = TweenMax.to('#animation-0', 0.3, {scale: 3});

  var tween1 = TweenMax.to('#animation-1', 2.0, {scale: 5});

  var tween2 = TweenMax.to('#animation-2', 0.4, {scale: 5,rotation: 360});

var tween3 = TweenMax.to('#animation-3', 0.4, {backgroundColor: 'rgb(17, 0, 98)',scale: 4,rotation: 360});

      var scene3 = new ScrollScene({
        triggerElement: '#scene-3',
        offset: 50
      })
      .setClassToggle('body', 'scene-3-active')
      .setTween(tween3)
      .addTo(scrollMagicController);





  // Add debug indicators fixed on right side
  scene3.addIndicators();
  
});