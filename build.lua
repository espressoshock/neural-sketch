#!/usr/bin/env texlua

module = "neural-sketch"
bundle = "neural-sketch"

uploadconfig = {
	author = "Vincenzo Buono",
	uploader = "Vincenzo Buono",
	email = "",
	pkg = "neural-sketch",
	version = "0.1",
	license = "lppl1.3c",
	summary = "A TikZ-based library for beautiful neural network and AI diagrams.",
	ctanPath = "/graphics/...",
	repository = "https://github.com/espressoshock/neural-sketch",
	bugtracker = "https://github.com/espressoshock/neural-sketch/issues",
	description = [[A LaTeX package that leverages TikZ to create publication-quality figures for
                  machine learning diagrams, system overviews, neural networks, algorithms, and more.]],
	update = true,
}

docfiledir = "doc"
sourcefiledir = "src"
typesetfiles = { "*.dtx", "*.tex" }
packtdszip = true -- recommended for "tree" layouts
