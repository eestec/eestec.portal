{ }:

with import <nixpkgs> {};

let
  base = {

  paths27 =
    [ git
      python27
      python27Packages.coverage
      python27Packages.flake8
      python27Packages.ipdb
      python27Packages.ipdbplugin
      python27Packages.ipython
      python27Packages.nose
      python27Packages.pylint
      python27Packages.recursivePthLoader
      python27Packages.sqlite3
      python27Packages.virtualenv
      stdenv
      zip
    ] ++ lib.attrValues python27.modules;

}; in base