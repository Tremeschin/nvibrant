{ pkgs ? import <nixpkgs> {} }:

pkgs.callPackage (
  { fetchFromGitHub, lib, pkgs, stdenv }:

  stdenv.mkDerivation rec {
    pname = "nvibrant";
    version = "1.1.0";

    nativeBuildInputs = with pkgs; [
      python313
      python313Packages.meson
      python313Packages.ninja
    ];

    srcs = [
      (lib.fileset.toSource {
        root = ./.;
        fileset = lib.fileset.unions [ ./nvibrant ./meson.build ];
      })
      (fetchFromGitHub {
        owner = "NVIDIA";
        repo = "open-gpu-kernel-modules";
        rev = "2af9f1f0f7de4988432d4ae875b5858ffdb09cc2";
        sha256 = "sha256-FGmMt3ShQrw4q6wsk8DSvm96ie5yELoDFYinSlGZcwQ=";
        name = "open-gpu";
      })
    ];

    sourceRoot = "source";

    postUnpack = ''
      cp -r open-gpu source/open-gpu
    '';

    buildPhase = ''
      meson setup --buildtype release ./build
      ninja -C ./build
    '';

    installPhase = ''
      mkdir -p $out/bin
      cp ./build/${pname} $out/bin
    '';
  }
) {}
