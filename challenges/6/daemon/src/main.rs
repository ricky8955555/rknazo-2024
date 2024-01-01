use anyhow::{anyhow, Result};
use hickory_server::authority::{Catalog, ZoneType};
use hickory_server::proto::rr::rdata::{PTR, SOA, TXT};
use hickory_server::proto::rr::{LowerName, Name, RData, RecordSet, RecordType, RrKey};
use hickory_server::store::in_memory::InMemoryAuthority;
use hickory_server::ServerFuture;
use litcrypt::{lc, use_litcrypt};
use once_cell::sync::Lazy;
use std::collections::BTreeMap;
use std::str::FromStr;
use std::sync::Arc;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, UdpSocket};

use_litcrypt!("l0okupTh3Dn5");

static FLAG: Lazy<String> = Lazy::new(|| lc!("flag{}"));

const DOMAIN: &str = "site.nazo.rk.";
const IP: &str = "127.69.60.1";
const REV: &str = "1.60.69.127.in-addr.arpa.";

async fn run_http_server_blocking() -> Result<()> {
    let listener = TcpListener::bind(format!("{IP}:80")).await?;
    let content = "the thing you're looking for is hidden in a service running at the address you requested. it records with the address you requested.\n你在找的东西藏在了你正在请求的地址的某个服务上, 并且它以某种形式使用了这个地址进行记录.\n";
    let content_length = content.len();
    loop {
        let (mut stream, _) = listener.accept().await?;
        let mut buf = [0; 16];
        stream.read_exact(&mut buf).await?;
        if !buf.starts_with(b"GET / HTTP/1.1") {
            stream
                .write_all(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                .await?;
            stream.shutdown().await?;
            continue;
        }
        let resp = format!("HTTP/1.1 200 OK\r\nContent-Length: {content_length}\r\n\r\n{content}");
        stream.write_all(resp.as_bytes()).await?;
    }
}

async fn run_dns_server_blocking() -> Result<()> {
    let mut catalog = Catalog::new();

    let ttl = 3600;
    let soa = RData::SOA(SOA::new(
        Name::from_str("ns.nazo.rk.")?,
        Name::from_str("noc.nazo.rk.")?,
        756296,
        3600,
        600,
        14400,
        3600,
    ));

    let mut records = BTreeMap::new();

    let mut set = RecordSet::new(&Name::from_str(DOMAIN)?, RecordType::SOA, 0);
    set.add_rdata(soa.clone());
    records.insert(
        RrKey::new(LowerName::from_str(DOMAIN)?, RecordType::SOA),
        set,
    );

    let mut set = RecordSet::with_ttl(Name::from_str(DOMAIN)?, RecordType::A, ttl);
    set.add_rdata(RData::A(IP.parse()?));
    records.insert(RrKey::new(LowerName::from_str(DOMAIN)?, RecordType::A), set);

    let mut set = RecordSet::with_ttl(Name::from_str(DOMAIN)?, RecordType::TXT, ttl);
    set.add_rdata(RData::TXT(TXT::new(vec![FLAG.to_string()])));
    records.insert(
        RrKey::new(LowerName::from_str(DOMAIN)?, RecordType::TXT),
        set,
    );

    let authority =
        InMemoryAuthority::new(Name::from_str(DOMAIN)?, records, ZoneType::Primary, false)
            .map_err(|e| anyhow!(e))?;

    catalog.upsert(LowerName::from_str(DOMAIN)?, Box::new(Arc::new(authority)));

    let mut records = BTreeMap::new();

    let mut set = RecordSet::new(&Name::from_str(REV)?, RecordType::SOA, 0);
    set.add_rdata(soa);
    records.insert(RrKey::new(LowerName::from_str(REV)?, RecordType::SOA), set);

    let mut set = RecordSet::with_ttl(Name::from_str(REV)?, RecordType::PTR, ttl);
    set.add_rdata(RData::PTR(PTR(Name::from_str(DOMAIN)?)));
    records.insert(RrKey::new(LowerName::from_str(REV)?, RecordType::PTR), set);

    let authority = InMemoryAuthority::new(Name::from_str(REV)?, records, ZoneType::Primary, false)
        .map_err(|e| anyhow!(e))?;

    catalog.upsert(LowerName::from_str(REV)?, Box::new(Arc::new(authority)));

    let mut server = ServerFuture::new(catalog);
    let socket = UdpSocket::bind(format!("{IP}:53")).await?;
    server.register_socket(socket);
    server.block_until_done().await?;

    Ok(())
}

#[tokio::main]
async fn main() -> Result<()> {
    _ = tokio::join!(
        tokio::spawn(run_dns_server_blocking()),
        tokio::spawn(run_http_server_blocking()),
    );
    Ok(())
}
