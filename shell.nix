with import <nixpkgs> {}; {
  qpidEnv = stdenvNoCC.mkDerivation {
    name = "dev-environment";
    buildInputs = [
        gcc13
        python312
    ];
  };
}