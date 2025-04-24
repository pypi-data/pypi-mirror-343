{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

let
  pkgs-unstable = import inputs.nixpkgs-unstable { system = pkgs.stdenv.system; };
in
{
  packages = [
    pkgs.git
    pkgs.bash
    pkgs.python312Packages.setuptools
  ];

  languages.python.enable = true;
  languages.python.uv.enable = true;
  languages.python.uv.package = pkgs-unstable.python312Packages.uv;
  languages.python.uv.sync.enable = true;
  languages.python.uv.sync.allExtras = true;
  languages.python.venv.enable = true;
  languages.python.version = "3.12";

  git-hooks.hooks = {
    shellcheck.enable = true;
    ruff.enable = true;
    ruff-format.enable = true;
    typos.enable = true;
    yamllint.enable = true;
    yamlfmt.enable = true;
    yamlfmt.settings.lint-only = false;
    check-toml.enable = true;
    commitizen.enable = true;
    nixfmt-rfc-style.enable = true;
    mdformat.enable = true;
    mdformat.package = pkgs.mdformat.withPlugins (
      ps: with ps; [
        mdformat-frontmatter
      ]
    );
    markdownlint.enable = true;
  };

  scripts.format.exec = ''
    yamlfmt .
    markdownlint --fix .
    pre-commit run --all-files
  '';

  scripts.test-all.exec = ''
    pytest -s -vv "$@"
  '';

  enterTest = ''
    test-all
  '';

  scripts.build.exec = ''
    uv build
  '';

  scripts.sample-pipeline-run.exec = ''
    python google_pipeline.py
  '';

  scripts.sample-pipeline-show.exec = ''
    dlt pipeline google_pipeline show
  '';
}
