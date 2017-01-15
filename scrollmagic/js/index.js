$(function() {
  
  var scrollMagicController = new ScrollMagic();
  
  var tween1 = TweenMax.to('#animation-1', 0.3, {
    backgroundColor: 'rgb(255, 39, 46)',
    scale: 10,
    rotation: 360
  });
  var scene1 = new ScrollScene({
    triggerElement: '#scene-1',
    offset: 50
  })
  .setClassToggle('body', 'scene-1-active')
  .setTween(tween1)
  .addTo(scrollMagicController);
  
    // Create Animation for 0.5s
  var tween2 = TweenMax.to('#animation-2', 0.3, {
    backgroundColor: 'rgb(0, 255, 187)',
    scale: 10,
    rotation: 360
  });
  
  var scene2 = new ScrollScene({
    triggerElement: '#scene-2',
		offset: 50
  })
  .setClassToggle('body', 'scene-2-active')
  .setTween(tween2)
  .addTo(scrollMagicController);
  
  
  
      // Create Animation for 0.5s
  var tween3 = TweenMax.to('#animation-3', 0.3, {
    backgroundColor: 'rgb(17, 0, 98)',
    scale: 10,
    rotation: 360
  });
  
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