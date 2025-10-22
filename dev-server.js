/**
 * dev-server - serves static resources for developing "earth" locally
 */

"use strict";

console.log("============================================================");
console.log(new Date().toISOString() + " - Starting");

var util = require("util");

/**
 * Returns true if the response should be compressed.
 */
function compressionFilter(req, res) {
    return (/json|text|javascript|font/).test(res.getHeader('Content-Type'));
}

/**
 * Adds headers to a response to enable caching.
 */
function cacheControl() {
    return function (req, res, next) {
        res.setHeader("Cache-Control", "public, max-age=300");
        return next();
    };
}

// Logger function removed - using morgan instead

var port = process.argv[2];
var express = require("express");
var compression = require("compression");
var morgan = require("morgan");
var app = express();

app.use(cacheControl());
app.use(compression({ filter: compressionFilter }));
app.use(morgan('combined'));
app.use(express.static("public"));

app.listen(port);
console.log("Listening on port " + port + "...");
