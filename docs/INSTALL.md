# Installation guide (on Ubuntu 16.04)

- [Installation guide (on Ubuntu 16.04)](#installation-guide-on-ubuntu-1604)
  - [Step 1: Install the dependencies](#step-1-install-the-dependencies)
  - [Step 2: Open port 631 for TCP traffic](#step-2-open-port-631-for-tcp-traffic)
  - [Step 3: Create a user account](#step-3-create-a-user-account)
  - [Step 4: Checkout the code](#step-4-checkout-the-code)
  - [Step 5: Setup Virtual Environment](#step-5-setup-virtual-environment)
  - [Step 6: Create a configuration file](#step-6-create-a-configuration-file)
  - [Step 7: Start the honeypot](#step-7-start-the-honeypot)
  - [Configure additional output plugins (OPTIONAL)](#configure-additional-output-plugins-optional)
  - [Change the default responses (OPTIONAL)](#change-the-default-responses-optional)
  - [Docker usage (OPTIONAL)](#docker-usage-optional)
  - [Command-line options](#command-line-options)
  - [Upgrading the honeypot](#upgrading-the-honeypot)

## Step 1: Install the dependencies

First we install system-wide support for Python virtual environments and other
dependencies. Actual Python packages are installed later.

```bash
sudo apt-get update
sudo apt-get install git python-virtualenv libffi-dev build-essential libpython-dev python2.7-minimal python3.5-minimal python-dev libmysqlclient-dev
```

## Step 2: Open port 631 for TCP traffic

If TCP port 631 is not aleady opened for incoming connections on your firewall
and router, you must open it now. While it is possible to have the honeypot
listen to this port directly, it is not advisable to do so. To begin with, it
means that the machine running the honeypot will become unable to use a printer
because normally the `cups` service for printing listens to this port and
you'd have to disable it. In addition, if the machine running the honeypot is
connected to an internal network (something that is not avisable by itself),
having the honeypot announce itself as a printer on this network could confuse
the other machines on it.

This is why we advise running the honeypot on some other port (e.g., 6631)
and using port redirection either from the NAT router or via `iptables` to
redirect the incoming port 631 traffic to it.

How exactly to do this from the NAT router depends on the router model;
please consult the instruction manual of the router. If the honeypot
machine is behind a NAT router, opening port 631 at the router must be
done in any case. The port redirection can be done either there or via
`iptables`. If you choose the latter approach, it can be done like this:

```bash
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 631 -j REDIRECT --to-port 6631
sudo iptables-save
```

Replace `eth0` with your actual network interface name. If you're unsure what
your network interface name is, try the command

```bash
ip route get 8.8.8.8
```

The network interface name should be the name after the word `dev` in the
output.

If you do decide to ignore our advice and run the honeypot on port 631 anyway,
there are some problems that need to be solved first. In particular, on Linux
processes owned by non-root users are not allowed to listen to ports lower
than 1024. One way to bypass this restriction is by using `authbind` but
even then you'll need to go through some hoops because even `authbind` has
some problems letting your non-root proccess listen to ports 512-1023.

From a user who can `sudo` (i.e., not from the user `ipphoney`), do the
following

```bash
sudo apt-get install authbind
sudo touch '/etc/authbind/byport/!631'
sudo chown ipphoney:ipphoney '/etc/authbind/byport/!631'
sudo chmod 770 '/etc/authbind/byport/!631'
```

Note how the file name is enclosed in single quotes and the port name
begins with an '!' character. This is necessary for `authbind` to allow
listening on a port that is in the 512-1023 range.

Then, at [step 7](#step-7-start-the-honeypot) , edit the file
`etc/honeypot-launch.cfg` and modify the `AUTHBIND_ENABLED` setting.

Again, we advise against using this approach.

## Step 3: Create a user account

It is strongly recommended to run the honeypot as a dedicated non-root user
(named `ipphoney` in our example), who cannot `sudo`:

```bash
$ sudo adduser --disabled-password ipphoney
Adding user 'ipphoney' ...
Adding new group 'ipphoney' (1002) ...
Adding new user 'ipphoney' (1002) with group 'ipphoney' ...
Changing the user information for ipphoney
Enter the new value, or press ENTER for the default
Full Name []:
Room Number []:
Work Phone []:
Home Phone []:
Other []:
Is the information correct? [Y/n]

$ sudo su - ipphoney
```

## Step 4: Checkout the code

```bash
$ git clone https://gitlab.com/bontchev/ipphoney.git
Cloning into 'ipphoney'...
remote: Enumerating objects: 116, done.
remote: Counting objects: 100% (116/116), done.
remote: Compressing objects: 100% (62/62), done.
remote: Total 116 (delta 56), reused 90 (delta 45), pack-reused 0
Receiving objects: 100% (116/116), 61.36 KiB | 1.75 MiB/s, done.
Resolving deltas: 100% (56/56), done.

$ cd ipphoney
```

## Step 5: Setup Virtual Environment

Next you need to create your virtual environment:

```bash
$ pwd
/home/ipphoney/ipphoney
$ virtualenv ipphoney-env
New python executable in ./ipphoney-env/bin/python
Installing setuptools, pip, wheel...done.
```

Activate the virtual environment and install the necessary dependencies

```bash
$ source ipphoney-env/bin/activate
(ipphoney-env) $ pip install --upgrade pip
(ipphoney-env) $ pip install --upgrade -r requirements.txt
```

## Step 6: Create a configuration file

The configuration for the honeypot is stored in `etc/honeypot.cfg.base` and
`etc/honeypot.cfg`. Both files are read on startup but the entries from
`etc/honeypot.cfg` take precedence. The `.base` file contains the default
settings and can be overwritten by upgrades, while `honeypot.cfg` will not be
touched. To run with a standard configuration, there is no need to change
anything.

For instance, in order to enable JSON logging, create `etc/honeypot.cfg` and
put in it only the following:

```honeypot.cfg
[output_jsonlog]
enabled = true
logfile = log/ipphoney.json
epoch_timestamp = true
```

For more information about how to configure additional output plugins (from
the available ones), please consult the appropriate `README.md` file in the
subdirectory corresponding to the plugin inside the `docs` directory.

## Step 7: Start the honeypot

Make a copy of the file `honeypot-launch.cfg.base`:

```bash
$ pwd
/home/ipphoney/ipphoney
$ cd etc
$ cp honeypot-launch.cfg.base honeypot-launch.cfg
$ cd ..
```

Before starting the honeypot, make sure that you have specified correctly
where it should look for the virtual environment. This documentation suggests
that you create it in `/home/ipphoney/ipphoney/ipphoney-env/`. If you
have indeed created it there, there is no need to change anything. If, however,
you have created it elsewhere, you have to edit the file
`/home/ipphoney/ipphoney/etc/honeypot-launch.cfg` and change the setting
of the variable `HONEYPOT_VIRTUAL_ENV` to point to the directory where your
virtual environment is.

Now you can launch the honeypot:

```bash
$ pwd
/home/ipphoney/ipphoney
$ ./bin/honeypot start
Starting the honeypot ...
The honeypot was started successfully.
```

## Configure additional output plugins (OPTIONAL)

The honeypot automatically outputs event data as text to the file
`log/honeypot.log`. Additional output plugins can be configured to record the
data other ways. Supported output plugins include:

- JSON
- MySQL
- SQLite3
- text

More plugins are likely to be added in the future.

See `docs/[Output Plugin]/README.md` for details.

## Change the default responses (OPTIONAL)

By default, the honeypot sends as responses to the various queries that it
emulates the contents of the files in the `responses` directory. Normally,
there is no need to change them. However, if you would like to modify the
responses to some operations, like what attributes the simulated printer
supports, you can do it by editing the files there. However, before touching
anything there, it is strongly recommended that you familiarize yourself
with the IPP protocol, so that the responses conform to what the attacking
system is expecting from a properly functioning IPP printer.

Each `IPP` file is a text file. Empty lines, leading and trailing spaces, and
lines beginning with the `#` character are ignored. Each file *must* begin
with a

```ipp
GROUP Operation-Attributes-Tag
```

line, *must* end with a

```ipp
GROUP End-of-Attributes-Tag
```

and *may* contain several `GROUP` and `ATTR` definitions.

In addition, the `ATTR` definitions can contain "macros". They are identifiers
starting with a `$`, wich are replaced with the following when the IPP script
is processed:

Macro | Replaced with
--- | ---
`$ip` | The current external IP address of the honeypot
`$now` | The current timestamp
`$old` | A random timestamp up to 30 days in the past

In other to prevent future updates of the honeypot from overwriting the
changes of these files made by the user, one should store the custom
responses in a separate directory and specify this directory either
in the `responses_dir=` directive of the `etc/honeypot.cfg` file or
via the `-r` command-line option.

The meaning of these response files is as follows:

File | Send as a response to the query
--- | ---
`getattr.ipp` | The mimimum set of required, recommended, and optional attributes for an IPP printer
`getattr_full.ipp` | The full set of attributes for an IPP printer (currently unused)
`getjobs.ipp` | The response to a `Get-Jobs` operation
`printjob.ipp` | The response to a `Print-Job` operation

## Docker usage (OPTIONAL)

First, from a user who can `sudo` (i.e., not from the user `ipphoney`) make
sure that `docker` is installed and that the user `ipphoney` is a member of
the `docker` group:

```bash
sudo apt-get install docker.io
sudo usermod -a -G docker ipphoney
```

**WARNING!** A user who belongs to the `docker` group has root user
privileges, which negates the advantages of creating the `ipphoney` user as a
restricted user in the first place. If a user is not a member of the `docker`
group, the only way for them to use Docker is via `sudo` - which a restricted
user like `ipphoney` cannot do. Since this increases the
[attack surface](https://docs.docker.com/engine/security/security/#docker-daemon-attack-surface),
we advise against using the honeypot with Docker. One alternative is to look
into other containerization systems that do not require privileged user access
in order to operate - e.g., [Podman](https://podman.io/).

Then switch to the user `ipphoney`, build the Docker image, and run it:

```bash
sudo su - ipphoney
docker build -t ipphoney .
docker run -d -p 6631:6631/tcp -u $(id -u):$(id -g) -v $(HOME}/ipphoney:/ipphoney -w /ipphoney ipphoney
```

## Command-line options

IPP Honey supports the following command-line options:

```options
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -p PORT, --port PORT  Port to listen on (default: 631)
  -l LOGFILE, --logfile LOGFILE
                        Log file (default: stdout)
  -r RESPONSES, --responses RESPONSES
                        Directory of the response files (default: responses)
  -d DLFOLDER, --dlfolder DLFOLDER
                        Directory for the uploaded samples (default: dl)  
  -s SENSOR, --sensor SENSOR
                        Sensor name (default: computer-name)
```

The settings specified via command-line options take precedence over the
corresponding settings in the `.cfg` files.

## Upgrading the honeypot

Updating is an easy process. First stop your honeypot. Then fetch any
available updates from the repository. As a final step upgrade your Python
dependencies and restart the honeypot:

```bash
./bin/honeypot stop
git pull
source ./ipphoney-env/bin/activate
pip install --upgrade -r requirements.txt
deactivate
./bin/honeypot start
```
