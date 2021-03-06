/*
 * Webshot: take a screenshot of the page at the given url
 * requires phantomjs
 */

var width = 800;
var height = 600;

var page = require('webpage').create();
var args = require('system').args;

var webshot = function(url, w, h) {
    page.viewportSize = { width: w, height: h };
    console.log("Webshot: loading page...");
    page.open(url, function(status) {
        if (status !== 'success') {
            console.log('Webshot: unable to load url: ' + url);
            //noinspection JSUnresolvedVariable Given by phantomjs
            phantom.exit()
        } else {
            window.setTimeout(function() {
                page.clipRect = { top: 170, left: 0, width: w, height: h };
                f = 'media/screen.jpg';
                page.evaluate(function() {
                    if ('transparent' === document.defaultView.getComputedStyle(document.body).getPropertyValue('background-color')) {
                        document.body.style.backgroundColor = '#fff';
                    }
                });
                console.log('Webshot: creating file: ' + f);
                page.render(f);
                phantom.exit()
            }, 200)
        }
    })
};

webshot(args[1], width, height);
