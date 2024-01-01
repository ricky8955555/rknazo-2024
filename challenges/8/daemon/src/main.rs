use anyhow::Result;
use litcrypt::{lc, use_litcrypt};
use once_cell::sync::Lazy;
use std::{
    fs,
    io::{BufRead, BufReader, Write},
    net::Shutdown,
    ops::Deref,
    os::unix::net::UnixListener,
    thread,
};

use_litcrypt!("c0mmW1thuN1xS0kit");

static FLAG: Lazy<String> = Lazy::new(|| lc!("flag{}"));

const SOCKET_PATH: &str = "/run/rknazo-sock.ctl";

fn main() -> Result<()> {
    _ = fs::remove_file(SOCKET_PATH);
    let listener = UnixListener::bind(SOCKET_PATH)?;

    for stream in listener.incoming() {
        let mut stream = stream?;
        thread::spawn(move || -> Result<()> {
            stream.write_all(b"welcome!\ntype 'help' to get help.\n\n")?;
            let buf = BufReader::new(stream.try_clone()?);
            stream.write_all(b">> ")?;
            for line in buf.lines() {
                let line = line?;
                match line.as_str() {
                    "flag" => {
                        stream.write_all(format!("{}\n", FLAG.deref()).as_bytes())?;
                    }
                    "help" => {
                        stream.write_all(b"help\t- show the help.\nflag\t- get the flag.\nexit\t- shutdown the session.\n")?;
                    }
                    "exit" => {
                        stream.write_all(b"bye~\n")?;
                        stream.shutdown(Shutdown::Both)?;
                    }
                    _ => {
                        stream.write_all(b"unknown instruction.\n")?;
                    }
                };
                stream.write_all(b">> ")?;
            }
            Ok(())
        });
    }

    Ok(())
}
