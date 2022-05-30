// ==UserScript==
// @name         Slither.io zoom only
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Enable zoom on slither.io without weird skins that don't work right or whatever
// @author       You
// @match        http://slither.io/
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    function zoom(e) {
        if (!window.gsc) { return; }
        if (!window.target_gsc) { window.target_gsc = window.gsc; }
        window.target_gsc *= Math.pow(0.9, e.wheelDelta / -120 || e.detail / 2 || 0);
        window.target_gsc > 2 ? window.target_gsc = 2 : window.target_gsc < 0.1 ? window.target_gsc = 0.1 : null;
    }

    if (/firefox/i.test(navigator.userAgent)) {
        document.addEventListener("DOMMouseScroll", zoom, false);
    } else {
        document.body.onmousewheel = zoom;
    }

    setInterval(function(){
        if (!window.target_gsc) {
            return;
        }
        window.gsc = window.target_gsc
    }, 25);


})();
