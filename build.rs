use std::io::Write;
use std::path::PathBuf;
use std::process::Command;

use rayon::prelude::*;
use anyhow::Result;

fn main() -> Result<()> {

    // Only make bindings when asked
    if std::env::var("BINDGEN").is_err() {
        return Ok(());
    }

    // Get common paths
    let root     = PathBuf::from(std::env::var("CARGO_MANIFEST_DIR")?);
    let opengpu  = root.join("open-gpu");
    let bindpath = root.join("nvibrant/driver");
    let bindmod  = bindpath.join("mod.rs");

    // Reset mod.rs, ensure dir exists
    std::fs::create_dir_all(&bindpath)?;
    std::fs::write(&bindmod, "")?;

    // Open mod.rs for appending
    let mut modfile = std::fs::OpenOptions::new()
        .append(true)
        .open(&bindmod)?;

    // Get all known driver versions
    let versions: Vec<String> = {
        let bytes = Command::new("git")
            .arg("tag")
            .arg("--sort=-version:refname")
            .current_dir(&opengpu)
            .output()?.stdout;

        String::from_utf8(bytes)?
            .lines().map(str::to_owned)
            .collect()
    };

    // Make bindings for each driver version
    versions.par_iter().for_each(|driver| {

        // Make bindings for this version
        Command::new("git").arg("checkout").arg(&driver)
            .current_dir(&opengpu)
            .output().unwrap();

        bindgen::Builder::default()

            // Relevant headers and structs
            .header("open-gpu/src/nvidia-modeset/interface/nvkms-ioctl.h")
            .header("open-gpu/src/nvidia-modeset/interface/nvkms-api.h")
            .clang_arg(format!("-Iopen-gpu/src/common/inc"))
            .clang_arg(format!("-Iopen-gpu/src/common/sdk/nvidia/inc"))
            .clang_arg(format!("-Iopen-gpu/src/common/unix/common/inc"))
            .allowlist_type("NvKms.*")

            // Minify sources
            .generate_comments(false)
            .layout_tests(false)
            .generate_inline_functions(false)
            .prepend_enum_name(false)
            .derive_debug(false)

            // Make and export
            .generate().unwrap()
            .write_to_file(bindpath.join(
                format!("v{}.rs", driver.replace('.', "_"))
            )).unwrap();
    });

    // Single threaded mod lol
    for driver in versions.iter() {
        writeln!(modfile, "pub mod v{};", driver.replace('.', "_"))?;
    }

    Ok(())
}
