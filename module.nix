{ isHomeModule ? false }:
{ config, lib, pkgs, ... }:

let
  inherit (lib)
    mkIf
    mkOption
    mkEnableOption
    mkPackageOption
    concatStringsSep
    types
  ;

  cfg = config.services.nvibrant;

  binPath = "${cfg.package}/bin/nvibrant";
  binArgs = concatStringsSep " " cfg.arguments;

  service = {
    Unit = {
      Description = "Apply nvibrant";
      After = [ "graphical.target" ];
    };
    Service = {
      Type = "oneshot";
      ExecStart = "${binPath} ${binArgs}";
    };
    Install.WantedBy = [ "default.target" ];
  };
in
{
  options.services.nvibrant = {
    enable = mkEnableOption "Enable nvibrant service";

    package = mkPackageOption pkgs "nvibrant" { };

    arguments = mkOption {
      type = types.listOf types.str;
      default = [ "0" ];
      example = [ "512" ];
      description = ''
        List of vibrancy levels to pass to nvibrant, ranging from `-1024`
        (greyscale) to `1023` (max saturation), matching the order of physical
        ports in your GPU.
      '';
    };
  };

  config = mkIf cfg.enable (
    if isHomeModule
    then {
      home.packages = [ cfg.package ];
      systemd.user.services.nvibrant = service;
    }
    else {
      environment.systemPackages = [ cfg.package ];
      systemd.services.nvibrant = service;
    }
  );
}
