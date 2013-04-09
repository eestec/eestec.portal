{ }:

let
  base = import ./base.nix { };

in

with import <nixpkgs> {};

buildEnv {
  name = "dev-env";
  paths =
    [
    ] ++ base.paths27;
}