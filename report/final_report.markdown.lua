local ran_ok, error = pcall(function() local kpse = require("kpse") kpse.set_program_name("luatex") local lfs = require("lfs") local cacheDir = "./_markdown_final_report" if not lfs.isdir(cacheDir) then assert(lfs.mkdir(cacheDir)) end local md = require("markdown") local convert = md.new({cacheDir = "./_markdown_final_report", smartEllipses = true, } ) local input = assert(io.open("README.md", "r"):read("*a")) print(convert(input:gsub("\r\n?", "\n") .. "\n")) end) if not ran_ok then local file = io.open("./final_report.markdown.err", "w") if file then file:write(error .. "\n") file:close() end print('\\markdownError{An error was encountered while executing Lua code}{For further clues, examine the file "./final_report.markdown.err"}') end