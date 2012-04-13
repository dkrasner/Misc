library(optparse)

options <- list(make_option(c('--client')),make_option(c('--infile')),default=NULL)
options <- parse_args(OptionParser(option_list = options))

print(options$client)