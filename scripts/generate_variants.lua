#!/usr/bin/env lua
-- Usage: lua generate_variants.lua <texfile> [target_directory]
-- This script requires pdflatex, pdf2svg, and mv (or an equivalent copy command on your system).

-- Check command-line arguments.
if #arg < 1 then
  print("Usage: lua " .. arg[0] .. " <texfile> [target_directory]")
  os.exit(1)
end

local texfile = arg[1]
local target_dir = arg[2] or "./"  -- default to current directory if not provided

-- Extract the filename (without path) from the provided tex file.
local filename = texfile:match("([^/\\]+)$")
if not filename then
  print("Invalid tex file name: " .. texfile)
  os.exit(1)
end

-- Extract the basename (filename without extension).
local basename = filename:match("(.+)%..+$")
if not basename then
  print("Invalid tex file name (extension missing): " .. texfile)
  os.exit(1)
end

-- Define temporary file names and output names.
local light_tex       = basename .. "_light.tex"
local dark_tex        = basename .. "_dark.tex"
local light_job       = basename .. "_light"
local dark_job        = basename .. "_dark"
local light_pdf       = light_job .. ".pdf"
local dark_pdf        = dark_job .. ".pdf"
local light_svg_temp  = light_job .. ".svg"
local dark_svg_temp   = dark_job .. ".svg"
local final_light_svg = target_dir .. "/" .. basename .. ".svg"
local final_dark_svg  = target_dir .. "/" .. basename .. "-dark.svg"

-- Helper function to run a shell command.
local function run_cmd(cmd)
  print("Running: " .. cmd)
  local ret = os.execute(cmd)
  if ret ~= 0 then
    print("Warning: Command returned a non-zero exit code: " .. cmd)
  end
  return ret
end

-- Helper function to check if a file exists.
local function file_exists(name)
  local f = io.open(name, "r")
  if f then
    f:close()
    return true
  else
    return false
  end
end

-- Function to modify the neural-sketch package option for dark-mode.
local function set_dark_mode_option(content, mode)
  local new_content, replacements = content:gsub(
    "(\\usepackage%s*%[)(.-)(%]{%s*neural%-sketch%s*})",
    function(prefix, options, suffix)
      local new_options = options:gsub("dark%-mode%s*=%s*[%a]+", "dark-mode=" .. mode)
      return prefix .. new_options .. suffix
    end
  )
  if replacements == 0 then
    print("Could not find \\usepackage[..]{neural-sketch} in " .. texfile)
    os.exit(1)
  end
  return new_content
end

-- Helper function to remove a file.
local function remove_file(fname)
  local ok, err = os.remove(fname)
  if not ok then
    print("Warning: Could not remove " .. fname .. ": " .. (err or "unknown error"))
  else
    print("Removed temporary file: " .. fname)
  end
end

-- Read the original LaTeX file.
local file = io.open(texfile, "r")
if not file then
  print("Error opening " .. texfile)
  os.exit(1)
end
local original_content = file:read("*all")
file:close()

-- Create the light variant (with dark-mode=false).
local light_content = set_dark_mode_option(original_content, "false")
file = io.open(light_tex, "w")
if not file then
  print("Error writing to " .. light_tex)
  os.exit(1)
end
file:write(light_content)
file:close()

-- Compile the light variant.
run_cmd("pdflatex -jobname=" .. light_job .. " -interaction=nonstopmode " .. light_tex)

-- Convert the generated light PDF to SVG if it exists.
if file_exists(light_pdf) then
  run_cmd("pdf2svg " .. light_pdf .. " " .. light_svg_temp)
else
  print("Warning: " .. light_pdf .. " not found after light variant compilation. Skipping SVG generation for light variant.")
end

-- Create the dark variant (with dark-mode=true).
local dark_content = set_dark_mode_option(original_content, "true")
file = io.open(dark_tex, "w")
if not file then
  print("Error writing to " .. dark_tex)
  os.exit(1)
end
file:write(dark_content)
file:close()

-- Compile the dark variant.
run_cmd("pdflatex -jobname=" .. dark_job .. " -interaction=nonstopmode " .. dark_tex)

-- Convert the generated dark PDF to SVG if it exists.
if file_exists(dark_pdf) then
  run_cmd("pdf2svg " .. dark_pdf .. " " .. dark_svg_temp)
else
  print("Warning: " .. dark_pdf .. " not found after dark variant compilation. Skipping SVG generation for dark variant.")
end

-- Move (and rename) the generated SVG files to the target directory.
if file_exists(light_svg_temp) then
  run_cmd("mv " .. light_svg_temp .. " " .. final_light_svg)
else
  print("Warning: " .. light_svg_temp .. " does not exist. Skipping move for the light SVG.")
end

if file_exists(dark_svg_temp) then
  run_cmd("mv " .. dark_svg_temp .. " " .. final_dark_svg)
else
  print("Warning: " .. dark_svg_temp .. " does not exist. Skipping move for the dark SVG.")
end

-- Clean up temporary tex and pdf files.
remove_file(light_tex)
remove_file(dark_tex)
remove_file(light_pdf)
remove_file(dark_pdf)

print("Script completed. Check the output SVGs in " .. target_dir)
