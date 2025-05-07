SELECT
  -- Raw columns
  "systemInfo.cpu"      AS raw_cpu,
  "systemInfo.gpu"      AS raw_gpu,
  "systemInfo.os"       AS raw_os,
  "systemInfo.unix_timestamp" AS unix_ts,

  -- 1) CPU vendor / Steam Deck APU detection
  CASE
    WHEN LOWER("systemInfo.cpu") LIKE '%custom apu%' THEN 'Steam Deck APU'
    WHEN LOWER("systemInfo.cpu") LIKE '%amd%'        THEN 'AMD'
    WHEN LOWER("systemInfo.cpu") LIKE '%intel%'      THEN 'Intel'
    ELSE 'Other'
  END AS cpu_vendor,

  -- 2) GPU vendor / Steam Deck GPU detection
  CASE
    WHEN LOWER("systemInfo.gpu") LIKE '%custom gpu%' THEN 'Steam Deck GPU'
    WHEN LOWER("systemInfo.gpu") LIKE '%nvidia%'    THEN 'NVIDIA'
    WHEN LOWER("systemInfo.gpu") LIKE '%amd%'       THEN 'AMD'
    ELSE 'Other'
  END AS gpu_vendor,

  -- 3) OS distribution (expanded list, including SteamOS)
  CASE
    WHEN LOWER("systemInfo.os") LIKE '%steamos%'       THEN 'SteamOS (Deck)'
    WHEN LOWER("systemInfo.os") LIKE '%arch%'          THEN 'Arch Linux'
    WHEN LOWER("systemInfo.os") LIKE '%gentoo%'        THEN 'Gentoo Linux'
    WHEN LOWER("systemInfo.os") LIKE '%debian%'        THEN 'Debian'
    WHEN LOWER("systemInfo.os") LIKE '%ubuntu%'        THEN 'Ubuntu'
    WHEN LOWER("systemInfo.os") LIKE '%fedora%'        THEN 'Fedora'
    WHEN LOWER("systemInfo.os") LIKE '%centos%'        THEN 'CentOS'
    WHEN LOWER("systemInfo.os") LIKE '%red hat%' 
         OR LOWER("systemInfo.os") LIKE '%rhel%'       THEN 'Red Hat'
    WHEN LOWER("systemInfo.os") LIKE '%opensuse%' 
         OR LOWER("systemInfo.os") LIKE '%suse%'       THEN 'openSUSE'
    WHEN LOWER("systemInfo.os") LIKE '%manjaro%'       THEN 'Manjaro'
    WHEN LOWER("systemInfo.os") LIKE '%mint%'          THEN 'Linux Mint'
    WHEN LOWER("systemInfo.os") LIKE '%elementary%'    THEN 'Elementary OS'
    WHEN LOWER("systemInfo.os") LIKE '%slackware%'     THEN 'Slackware'
    WHEN LOWER("systemInfo.os") LIKE '%pop!_os%' 
         OR LOWER("systemInfo.os") LIKE '%pop os%'     THEN 'Pop!_OS'
    ELSE "systemInfo.os"
  END AS os_distribution,

  -- 4) Device type: Steam Deck vs. everything else
  CASE
    WHEN LOWER("systemInfo.cpu") LIKE '%custom apu%'
         OR LOWER("systemInfo.os")  LIKE '%steamos%' THEN 'Steam Deck'
    ELSE 'Non‑Deck'
  END AS device_type,

  -- 5) Human‑readable timestamp (UTC)
  datetime("systemInfo.unix_timestamp", 'unixepoch') 
    AS readable_timestamp

FROM reports;   -- make sure this matches your actual table name

