use std::{net::UdpSocket, time::Duration, thread};
use anyhow::Result;
use litcrypt::{lc, use_litcrypt};
use once_cell::sync::Lazy;

use_litcrypt!("br0@dkaStAdDr3ss");

static FLAG: Lazy<String> = Lazy::new(|| lc!("flag{}"));

fn main() -> Result<()> {
    let socket = UdpSocket::bind("0.0.0.0:0")?;
    socket.set_broadcast(true)?;
    socket.connect(("255.255.255.255", 0))?;
    loop {
        socket.send(FLAG.as_bytes())?;
        thread::sleep(Duration::from_secs(3));
    }
}
