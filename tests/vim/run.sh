#!/usr/bin/env bash
pipx run covimerage run --report-options '--show-missing' vim -Nu vimrc -Es -c 'Vader! *.vader'
