#!/usr/bin/env texlua

module = "neural-sketch"
-- bundle = "neural-sketch"

uploadconfig = {
	author = "Vincenzo Buono",
	uploader = "Vincenzo Buono",
	email = "vincenzo.buono@hh.se",
	pkg = "neural-sketch",
	version = "0.8",
	license = "lppl1.3c",
	summary = "An elegant LaTeX package leveraging TikZ to produce publication-ready diagrams, optimized for AI and machine learning visualizations",
  ctanPath = "/graphics/pgf/contrib/neural-sketch",
	repository = "https://github.com/espressoshock/neural-sketch",
	bugtracker = "https://github.com/espressoshock/neural-sketch/issues",
	description = [[
    Neural-Sketch is a modern, opinionated yet highly customizable LaTeX package specifically designed for creating publication-quality diagrams commonly found in AI, machine learning, and technical documents. Leveraging TikZ alongside contemporary LaTeX3 paradigms (expl3, l3keys), it simplifies the creation of complex figures such as neural network architectures, flowcharts, system overviews, and algorithmic visualizations.
  ]],
	summary = "A TikZ-based library ",
  topics = { "diagrams", "graphics", "pgf", "tikz", "latex3", "machine learning", "publication" },
	update = true,
}

docfiledir = "doc"
sourcefiledir = "src"
typesetfiles = { "*.dtx", "*.tex" }
packtdszip = true -- recommended for "tree" layouts
