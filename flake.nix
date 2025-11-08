{
  description = "nvibrant flake";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      supportedSystems = [ "x86_64-linux" ];

      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (
        system: f nixpkgs.legacyPackages.${system}
      );

      createPackage = import ./default.nix;
      createModule = import ./module.nix;
    in {
      formatter = forAllSystems (pkgs: pkgs.alejandra);

      packages = forAllSystems (pkgs: rec {
        nvibrant = createPackage { inherit pkgs; };
        default = nvibrant;
      });

      overlays.default = (final: _: {
        nvibrant = createPackage { pkgs = final; };
      });

      nixosModules.default = createModule { };
      homeModules.default = createModule { isHomeModule = true; };
    };
}
