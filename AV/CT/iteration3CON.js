/*global ODSA */
// Written by Jieun Chon
//Array-Based list introduction
$(document).ready(function() {
  "use strict";
  var arrValues = [4, 13, 6, 9, 11];
  var av_name = "iteration3CON";
  var interpret = ODSA.UTILS.loadConfig({av_name: av_name}).interpreter;
  var av = new JSAV(av_name);
  var leftMargin = 270,
      rect_left = leftMargin - 150,
      rect0_top = 0,
      rect_top = 40,
      topMargin = rect_top + 20;

  var nodegap = 40;


  // blue boxes, floor 1
  var topblue = av.g.rect(rect_left, rect0_top, 280, 35, 10).addClass("bluebox");
  var botblue = av.g.rect(rect_left, rect0_top + 295, 280, 35, 10).addClass("bluebox");

  // floor 2
  av.g.rect(rect_left, rect_top, 250, 35, 10).addClass("box");
  av.g.rect(rect_left, rect_top + 20, 50, 15).addClass("box"); // for no-roung on the corner

  //floor 3 and the JSAV array contains arrValues
  av.g.rect(rect_left, rect_top + 25, 30, 60, 10).addClass("box").css({opacity: 0.9});
  av.g.rect(rect_left + 73, rect_top + 25, 30, 60, 10).addClass("box").css({opacity: 0.9});
  var arr = av.ds.array(arrValues, {indexed: false, left: leftMargin, top: topMargin, position: "absolute"});

  //floor 4, long purple
  av.g.rect(rect_left, rect_top + 76, 300, 30, 10).addClass("box");

  //floor 5, left big purple box
  av.g.rect(rect_left, rect_top + 80, 110, 170, 10).addClass("box");
  av.g.rect(rect_left, rect_top + 76, 50, 15).addClass("box");

  //mid blue/calculate boxes ( and "set total = ..." blue box )
  var midblue1 = av.g.rect(rect_left + 130, rect_top + 120, 130, 66, 10).addClass("bluebox");
  var midblue2 = av.g.rect(rect_left + 220, rect_top + 139, 20, 32, 15).addClass("calbox");
  var midblue3 = av.g.rect(rect_left + 240, rect_top + 120, 120, 66, 10).addClass("calbox");

  // last purple floor
  av.g.rect(rect_left + 90, rect_top + 200, 240, 50, 10).addClass("box");


// ------------------ labels ------------------------

  var initlabel = av.label("set total = 0", {left: rect_left + 5, top: rect_top - 65});
  initlabel.addClass("labels").addClass("midlabel");

  var label1 = av.label("for each item", {left: rect_left + 5, top: rect_top - 30});
  label1.addClass("labels");

  var label2 = av.label("price", {left: rect_left + 19, top: rect_top + 45});
  label2.addClass("labels");

  var label3 = av.label("do", {left: rect_left + 35, top: rect_top + 100});
  label3.addClass("labels");

  var pricelabel = av.label("set total = total + price", {left: rect_left + 140, top: rect_top + 117});
  pricelabel.addClass("labels");
  pricelabel.addClass("smalllabel");

  var valuelabel = av.label("", {left: rect_left + 390, top: rect_top + 111});
  valuelabel.addClass("labels");
  valuelabel.addClass("valuelabel");


  // <<--------------- STATE BOX ----------------->>

  var stateX = 700;
  var stateY = - 20;
  var stateLabel = av.label("STATE", {left: stateX, top: stateY});
  stateLabel.addClass("statelabel");

  var stateBox = av.g.rect(stateX - 25, stateY + 50, 110, 280).addClass("statebox");

  // price box and label
  av.label("PRICE", {left: stateX + 5, top: stateY + 65});
  stateLabel.addClass("statelabel");

  var priceBox = av.g.rect(stateX - 5, stateY + 105, 70, 70).addClass("bluebox");

  var priceBoxLabel = av.label("", {left: stateX + 23, top: stateY + 100});
  priceBoxLabel.addClass("labels");
  priceBoxLabel.addClass("midlabel");

  // total box and label
  av.label("TOTAL", {left: stateX + 5, top: stateY + 180});
  stateLabel.addClass("statelabel");

  var totalBox = av.g.rect(stateX - 5, stateY + 220, 70, 70).addClass("bluebox");
  var totalBoxLabel = av.label("", {left: stateX + 23, top: stateY + 215});

  totalBoxLabel.addClass("labels");
  totalBoxLabel.addClass("midlabel");

  // <<--------- Slide Show <<--------->>


  // Slide 1
  av.umsg(interpret("sc1"));
  var nextleft = leftMargin - 120;
  av.displayInit();


  // Slide 2
  av.umsg(interpret("sc2"));
  topblue.addClass("blueboxhigh");
  topblue.removeClass("blueboxhigh");

  totalBox.addClass("blueboxhigh");
  totalBox.removeClass("blueboxhigh");
  totalBoxLabel.value("0");
  av.step();

  // Slide 3
  av.umsg(interpret("sc3"));
  arr.css({left: nextleft});   //move array
  nextleft -= nodegap; // calculate nextleft value for next array moving
  priceBoxLabel.value(" 4 ")
  priceBox.addClass("blueboxhigh");
  priceBox.removeClass("blueboxhigh");
  av.step();

  // Slide 4
  av.umsg(interpret("sc4"));
  midblue2.addClass("calboxhigh");
  midblue2.removeClass("calboxhigh");
  midblue3.addClass("calboxhigh");
  midblue3.removeClass("calboxhigh");
  valuelabel.value("0 + 4");
  av.step();

  // Slide 5
  av.umsg(interpret("sc5"));
  midblue1.addClass("calboxhigh");
  midblue1.removeClass("calboxhigh");
  totalBox.addClass("blueboxhigh");
  totalBox.removeClass("blueboxhigh");
  totalBoxLabel.value(" 4 ");
  // totallabel.css({left: stateX + 9});
  av.step();


  // Slide 6
  av.umsg(interpret("sc6"));
  arr.css({left: nextleft});
  nextleft -= nodegap;
  priceBox.addClass("blueboxhigh");
  priceBox.removeClass("blueboxhigh");
  priceBoxLabel.value(" 13 ");
  priceBoxLabel.css({left: stateX + 18});
  av.step();

  // Slide 7
  av.umsg(interpret("sc7"));
  midblue2.addClass("calboxhigh");
  midblue2.removeClass("calboxhigh");
  midblue3.addClass("calboxhigh");
  midblue3.removeClass("calboxhigh");
  valuelabel.value(" 4 + 13 ");
  av.step();


  // Slide 8
  av.umsg(interpret("sc8"));
  totalBoxLabel.value(" 21 ");
  totalBoxLabel.css({left: stateX +18});
  midblue1.addClass("calboxhigh");
  midblue1.removeClass("calboxhigh");
  totalBox.addClass("blueboxhigh");
  totalBox.removeClass("blueboxhigh");
  av.step();

  // Slide 9
  av.umsg(interpret("sc9"));
  arr.css({left: nextleft});
  nextleft -= nodegap;
  priceBox.addClass("blueboxhigh");
  priceBox.removeClass("blueboxhigh");
  priceBoxLabel.value(" 6 ");
  priceBoxLabel.css({left: stateX + 23});
  av.step();

  // Slide 10
  av.umsg(interpret("sc10"));
  midblue2.addClass("calboxhigh");
  midblue2.removeClass("calboxhigh");
  midblue3.addClass("calboxhigh");
  midblue3.removeClass("calboxhigh");
  valuelabel.value(" 21 + 6 ");
  av.step();

  // Slide 11
  av.umsg(interpret("sc11"));
  totalBoxLabel.value(" 27 ");
  midblue1.addClass("calboxhigh");
  midblue1.removeClass("calboxhigh");
  totalBox.addClass("blueboxhigh");
  totalBox.removeClass("blueboxhigh");
  av.step();

  // Slide 12
  av.umsg(interpret("sc12"));
  arr.css({left: nextleft});
  nextleft -= nodegap;
  priceBox.addClass("blueboxhigh");
  priceBox.removeClass("blueboxhigh");
  priceBoxLabel.value(" 9 ");
  av.step();

  // Slide 13
  av.umsg(interpret("sc13"));
  midblue2.addClass("calboxhigh");
  midblue2.removeClass("calboxhigh");
  midblue3.addClass("calboxhigh");
  midblue3.removeClass("calboxhigh");
  valuelabel.value(" 27 + 9 ");
  av.step();

  // Slide 14
  av.umsg(interpret("sc14"));
  totalBoxLabel.value(" 36 ");
  midblue1.addClass("calboxhigh");
  midblue1.removeClass("calboxhigh");
  totalBox.addClass("blueboxhigh");
  totalBox.removeClass("blueboxhigh");
  av.step();

  // Slide 15
  av.umsg(interpret("sc15"));
  arr.css({left: nextleft});
  nextleft -= (nodegap + 50);
  priceBox.addClass("blueboxhigh");
  priceBox.removeClass("blueboxhigh");
  priceBoxLabel.value(" 11 ");
  priceBoxLabel.css({left: stateX + 18});
  av.step();

  // Slide 16
  av.umsg(interpret("sc16"));
  midblue2.addClass("calboxhigh");
  midblue2.removeClass("calboxhigh");
  midblue3.addClass("calboxhigh");
  midblue3.removeClass("calboxhigh");
  valuelabel.value(" 36 + 11 ");
  av.step();

  // Slide 17
  av.umsg(interpret("sc17"));
  totalBoxLabel.value(" 47 ");
  midblue1.addClass("calboxhigh");
  midblue1.removeClass("calboxhigh");
  totalBox.addClass("blueboxhigh");
  totalBox.removeClass("blueboxhigh");
  av.step();
  //
  // Slide 18
  av.umsg(interpret("sc18"));
  arr.css({left: nextleft});
  // priceBoxLabel.value("");
  valuelabel.value("");
  av.step();

  // Slide 19
  av.umsg(interpret("sc19"));
  botblue.addClass("blueboxhigh");
  botblue.removeClass("blueboxhigh");
  av.recorded();

  //last Slide
    av.recorded();
});
