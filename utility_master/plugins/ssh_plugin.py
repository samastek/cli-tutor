"""Plugin for teaching the 'ssh' command and its various options."""

import re
from typing import List

from utility_master.core.base_plugin import BasePlugin, Task, TaskResult


class SshPlugin(BasePlugin):
    """Plugin for learning the ssh command."""
    
    def get_name(self) -> str:
        return "SSH Command Learning Plugin"
    
    def get_description(self) -> str:
        return "Learn the ssh command for secure remote connections and file transfers"
    
    def get_utility_name(self) -> str:
        return "ssh"
    
    def get_tasks(self, difficulty: str = "all") -> List[Task]:
        """Return ssh learning tasks."""
        all_tasks = [
            # Beginner tasks
            Task(
                id="ssh_basic",
                description="Connect to a remote server with username 'user' and hostname 'example.com'",
                expected_command="ssh user@example.com",
                difficulty="beginner",
                hints=["Use the format: ssh username@hostname", "Basic syntax: ssh user@server"]
            ),
            Task(
                id="ssh_port",
                description="Connect to 'server.com' as user 'admin' on port 2222",
                expected_command="ssh -p 2222 admin@server.com",
                difficulty="beginner",
                hints=["Use the -p option to specify a port", "Format: ssh -p PORT user@host"]
            ),
            Task(
                id="ssh_key",
                description="Connect to 'myserver.net' as 'deploy' using the private key file '~/.ssh/id_rsa'",
                expected_command="ssh -i ~/.ssh/id_rsa deploy@myserver.net",
                difficulty="beginner",
                hints=["Use the -i option to specify a key file", "Format: ssh -i keyfile user@host"]
            ),
            Task(
                id="ssh_ipv4_only",
                description="Connect to 'dual.stack.com' as 'admin' forcing IPv4 connection only",
                expected_command="ssh -4 admin@dual.stack.com",
                difficulty="beginner",
                hints=["Use -4 to force IPv4", "This is useful when you have IPv6 issues"]
            ),
            Task(
                id="ssh_quiet_mode",
                description="Connect to 'prod.server.com' as 'deploy' in quiet mode (suppress warnings)",
                expected_command="ssh -q deploy@prod.server.com",
                difficulty="beginner",
                hints=["Use -q for quiet mode", "This suppresses warning and diagnostic messages"]
            ),
            
            # Intermediate tasks
            Task(
                id="ssh_verbose",
                description="Connect to 'debug.com' as 'root' with verbose output for troubleshooting",
                expected_command="ssh -v root@debug.com",
                difficulty="intermediate",
                hints=["Use the -v option for verbose output", "This helps with debugging connection issues"]
            ),
            Task(
                id="ssh_no_host_check",
                description="Connect to 'test.local' as 'user' without strict host key checking",
                expected_command="ssh -o StrictHostKeyChecking=no user@test.local",
                difficulty="intermediate",
                hints=["Use -o to set SSH options", "StrictHostKeyChecking=no disables host key verification"]
            ),
            Task(
                id="ssh_tunnel_local",
                description="Create a local port forward from local port 8080 to remote port 80 on 'webserver.com' as user 'www'",
                expected_command="ssh -L 8080:localhost:80 www@webserver.com",
                difficulty="intermediate",
                hints=["Use -L for local port forwarding", "Format: -L localport:remotehost:remoteport"]
            ),
            Task(
                id="ssh_execute_command",
                description="Execute the command 'uptime' on remote server 'monitor.com' as user 'ops'",
                expected_command="ssh ops@monitor.com uptime",
                difficulty="intermediate",
                hints=["Add the command after the hostname", "Format: ssh user@host command"]
            ),
            Task(
                id="ssh_x11_forward",
                description="Connect to 'desktop.lan' as 'gui' with X11 forwarding enabled",
                expected_command="ssh -X gui@desktop.lan",
                difficulty="intermediate",
                hints=["Use -X for X11 forwarding", "This allows running GUI applications remotely"]
            ),
            Task(
                id="ssh_agent_forward",
                description="Connect to 'jump.host.com' as 'admin' with SSH agent forwarding enabled",
                expected_command="ssh -A admin@jump.host.com",
                difficulty="intermediate",
                hints=["Use -A for agent forwarding", "This allows using your local SSH keys on remote hosts"]
            ),
            Task(
                id="ssh_timeout_connect",
                description="Connect to 'slow.server.com' as 'user' with a connection timeout of 10 seconds",
                expected_command="ssh -o ConnectTimeout=10 user@slow.server.com",
                difficulty="intermediate",
                hints=["Use -o ConnectTimeout=seconds", "This prevents hanging on slow connections"]
            ),
            Task(
                id="ssh_keepalive",
                description="Connect to 'firewall.corp.com' as 'vpn' with server alive interval of 60 seconds",
                expected_command="ssh -o ServerAliveInterval=60 vpn@firewall.corp.com",
                difficulty="intermediate",
                hints=["Use ServerAliveInterval to prevent disconnections", "This sends keepalive packets"]
            ),
            Task(
                id="ssh_batch_mode",
                description="Connect to 'auto.deploy.com' as 'ci' in batch mode (no password/passphrase prompts)",
                expected_command="ssh -o BatchMode=yes ci@auto.deploy.com",
                difficulty="intermediate",
                hints=["Use BatchMode=yes for non-interactive sessions", "Useful for automated scripts"]
            ),
            
            # Advanced tasks
            Task(
                id="ssh_background",
                description="Connect to 'gateway.com' as 'proxy' and run in background with no command execution",
                expected_command="ssh -f -N proxy@gateway.com",
                difficulty="advanced",
                hints=["Use -f to run in background", "Use -N to not execute remote commands"]
            ),
            Task(
                id="ssh_dynamic_tunnel",
                description="Create a dynamic SOCKS proxy on local port 1080 through 'proxy.com' as user 'tunnel'",
                expected_command="ssh -D 1080 tunnel@proxy.com",
                difficulty="advanced",
                hints=["Use -D for dynamic port forwarding", "This creates a SOCKS proxy"]
            ),
            Task(
                id="ssh_multiple_options",
                description="Connect to 'secure.gov' as 'admin' on port 443, using key file '/home/admin/.ssh/gov_key', with compression and verbose output",
                expected_command="ssh -p 443 -i /home/admin/.ssh/gov_key -C -v admin@secure.gov",
                difficulty="advanced",
                hints=["Combine multiple options: -p, -i, -C, -v", "Use -C for compression"]
            ),
            Task(
                id="ssh_remote_forward",
                description="Create a remote port forward from remote port 9090 to local port 3000 on 'build.com' as user 'ci'",
                expected_command="ssh -R 9090:localhost:3000 ci@build.com",
                difficulty="advanced",
                hints=["Use -R for remote port forwarding", "Format: -R remoteport:localhost:localport"]
            ),
            Task(
                id="ssh_config_file",
                description="Connect using a specific SSH config file '/etc/ssh/special_config' to 'server.org' as 'service'",
                expected_command="ssh -F /etc/ssh/special_config service@server.org",
                difficulty="advanced",
                hints=["Use -F to specify a config file", "This overrides the default SSH config"]
            ),
            Task(
                id="ssh_jump_host",
                description="Connect to 'internal.server' as 'user' via jump host 'bastion.company.com' with user 'jump'",
                expected_command="ssh -J jump@bastion.company.com user@internal.server",
                difficulty="advanced",
                hints=["Use -J for ProxyJump", "Format: -J jumpuser@jumphost finaluser@finalhost"]
            ),
            Task(
                id="ssh_control_master",
                description="Connect to 'shared.host.com' as 'multi' with ControlMaster auto and ControlPath '/tmp/ssh-%r@%h:%p'",
                expected_command="ssh -o ControlMaster=auto -o ControlPath=/tmp/ssh-%r@%h:%p multi@shared.host.com",
                difficulty="advanced",
                hints=["ControlMaster allows connection sharing", "ControlPath specifies the socket file"]
            ),
            Task(
                id="ssh_cipher_selection",
                description="Connect to 'legacy.system.com' as 'old' using only aes256-ctr cipher",
                expected_command="ssh -c aes256-ctr old@legacy.system.com",
                difficulty="advanced",
                hints=["Use -c to specify cipher", "This is useful for legacy systems"]
            ),
            Task(
                id="ssh_multiple_tunnels",
                description="Connect to 'multi.tunnel.com' as 'tunnel' with local forwards 8080:localhost:80 and 3306:db.local:3306",
                expected_command="ssh -L 8080:localhost:80 -L 3306:db.local:3306 tunnel@multi.tunnel.com",
                difficulty="advanced",
                hints=["You can use multiple -L options", "Each -L creates a separate tunnel"]
            ),
            Task(
                id="ssh_escape_sequence",
                description="Connect to 'nested.ssh.com' as 'hop' with escape character set to '^X' (Control-X)",
                expected_command="ssh -e ^X hop@nested.ssh.com",
                difficulty="advanced",
                hints=["Use -e to set escape character", "Useful when SSHing through multiple hops"]
            ),
            Task(
                id="ssh_known_hosts",
                description="Connect to 'new.host.com' as 'first' using a specific known_hosts file '/tmp/known_hosts'",
                expected_command="ssh -o UserKnownHostsFile=/tmp/known_hosts first@new.host.com",
                difficulty="advanced",
                hints=["UserKnownHostsFile specifies the known_hosts location", "Useful for isolated environments"]
            ),
            Task(
                id="ssh_proxy_command",
                description="Connect to 'behind.nat.com' as 'hidden' using ProxyCommand 'nc -x proxy.com:8080 %h %p'",
                expected_command="ssh -o ProxyCommand='nc -x proxy.com:8080 %h %p' hidden@behind.nat.com",
                difficulty="advanced",
                hints=["ProxyCommand allows custom connection methods", "%h and %p are replaced with host and port"]
            ),
            Task(
                id="ssh_bind_address",
                description="Create a local tunnel on port 8888 bound to all interfaces (0.0.0.0) forwarding to remote port 80 on 'web.internal.com' as user 'forward'",
                expected_command="ssh -L 0.0.0.0:8888:localhost:80 forward@web.internal.com",
                difficulty="advanced",
                hints=["Specify bind address before local port", "0.0.0.0 allows external connections to tunnel"]
            ),
            Task(
                id="ssh_mac_algorithm",
                description="Connect to 'secure.bank.com' as 'audit' using only hmac-sha2-256 MAC algorithm and aes256-ctr cipher",
                expected_command="ssh -m hmac-sha2-256 -c aes256-ctr audit@secure.bank.com",
                difficulty="advanced",
                hints=["Use -m for MAC algorithm", "Combine with -c for cipher selection"]
            ),
            Task(
                id="ssh_compression_level",
                description="Connect to 'slow.link.org' as 'remote' with maximum compression level (9)",
                expected_command="ssh -C -o CompressionLevel=9 remote@slow.link.org",
                difficulty="advanced",
                hints=["Use -C to enable compression", "CompressionLevel can be 1-9"]
            )
        ]
        
        if difficulty == "all":
            return all_tasks
        else:
            return [task for task in all_tasks if task.difficulty == difficulty]
    
    def validate_task(self, task: Task, user_input: str) -> TaskResult:
        """Validate user input for ssh tasks."""
        user_input = user_input.strip()
        expected = task.expected_command
        
        # Normalize the commands for comparison
        user_normalized = self._normalize_ssh_command(user_input)
        expected_normalized = self._normalize_ssh_command(expected)
        
        success = user_normalized == expected_normalized
        score = 100 if success else 0
        feedback = ""
        
        if not success:
            feedback = self._generate_feedback(task, user_input, expected)
            # Partial credit for close attempts
            if user_input.startswith("ssh"):
                score = 20
                if self._has_correct_host(user_input, expected):
                    score = max(score, 40)
                if self._has_correct_options(user_input, expected):
                    score = max(score, 60)
        
        return TaskResult(
            success=success,
            user_input=user_input,
            expected=expected,
            feedback=feedback,
            score=score
        )
    
    def _normalize_ssh_command(self, command: str) -> str:
        """Normalize ssh command for comparison."""
        # Remove extra spaces
        command = ' '.join(command.split())
        
        if command.startswith('ssh '):
            parts = command.split()
            cmd = parts[0]
            options = []
            option_args = {}
            host_and_command = []
            
            i = 1
            while i < len(parts):
                part = parts[i]
                if part.startswith('-') and len(part) == 2:
                    option = part[1]
                    if option in 'piFLoRD':  # Options that take arguments
                        if i + 1 < len(parts):
                            option_args[option] = parts[i + 1]
                            i += 2
                        else:
                            i += 1
                    else:
                        options.append(option)
                        i += 1
                elif part.startswith('-o'):
                    # Handle -o options
                    if i + 1 < len(parts):
                        option_args['o'] = parts[i + 1]
                        i += 2
                    else:
                        i += 1
                else:
                    # Everything else (host and commands)
                    host_and_command.extend(parts[i:])
                    break
            
            # Rebuild command with sorted options
            result = [cmd]
            
            # Add options with arguments first, sorted by option letter
            for opt in sorted(option_args.keys()):
                if opt == 'o':
                    result.extend(['-o', option_args[opt]])
                else:
                    result.extend([f'-{opt}', option_args[opt]])
            
            # Add simple options, sorted
            if options:
                options.sort()
                for opt in options:
                    result.append(f'-{opt}')
            
            # Add host and commands
            result.extend(host_and_command)
            
            return ' '.join(result)
        
        return command
    
    def _has_correct_host(self, user_input: str, expected: str) -> bool:
        """Check if user input has the correct host."""
        user_host = self._extract_host(user_input)
        expected_host = self._extract_host(expected)
        return user_host == expected_host
    
    def _extract_host(self, command: str) -> str:
        """Extract the host part from SSH command."""
        parts = command.split()
        i = 1
        while i < len(parts):
            part = parts[i]
            if part.startswith('-'):
                if len(part) == 2 and i + 1 < len(parts):
                    option = part[1]
                    if option in 'piFLRDJecm':  # Options that take arguments
                        i += 2
                    elif option == 'o' and i + 1 < len(parts):
                        i += 2
                    else:
                        i += 1
                else:
                    i += 1
            else:
                # This should be the host (or user@host)
                return part
            
        return ""
    
    def _has_correct_options(self, user_input: str, expected: str) -> bool:
        """Check if user input has the correct options."""
        user_options = self._extract_options(user_input)
        expected_options = self._extract_options(expected)
        return user_options == expected_options
    
    def _extract_options(self, command: str) -> dict:
        """Extract options from SSH command."""
        parts = command.split()
        options = {}
        
        i = 1
        while i < len(parts):
            part = parts[i]
            if part.startswith('-') and len(part) == 2:
                option = part[1]
                if option in 'piFLRDJecm':  # Options that take arguments
                    if i + 1 < len(parts):
                        if option in 'LRD':  # These can have multiple values
                            if option not in options:
                                options[option] = []
                            options[option].append(parts[i + 1])
                        else:
                            options[option] = parts[i + 1]
                        i += 2
                    else:
                        options[option] = None
                        i += 1
                else:
                    options[option] = True
                    i += 1
            elif part.startswith('-o'):
                if i + 1 < len(parts):
                    if 'o' not in options:
                        options['o'] = []
                    options['o'].append(parts[i + 1])
                    i += 2
                else:
                    i += 1
            else:
                break
        
        return options
    
    def _generate_feedback(self, task: Task, user_input: str, expected: str) -> str:
        """Generate helpful feedback for incorrect answers."""
        if not user_input.startswith('ssh'):
            return "Remember to start with the 'ssh' command."
        
        feedback_parts = []
        
        # Check host
        if not self._has_correct_host(user_input, expected):
            expected_host = self._extract_host(expected)
            user_host = self._extract_host(user_input)
            if expected_host:
                if user_host:
                    feedback_parts.append(f"Incorrect host. Expected: {expected_host}, got: {user_host}")
                else:
                    feedback_parts.append(f"Missing host. Expected: {expected_host}")
        
        # Check options
        if not self._has_correct_options(user_input, expected):
            expected_options = self._extract_options(expected)
            user_options = self._extract_options(user_input)
            
            missing_options = set(expected_options.keys()) - set(user_options.keys())
            extra_options = set(user_options.keys()) - set(expected_options.keys())
            
            if missing_options:
                feedback_parts.append(f"Missing options: {', '.join(f'-{opt}' for opt in sorted(missing_options))}")
            
            if extra_options:
                feedback_parts.append(f"Extra options: {', '.join(f'-{opt}' for opt in sorted(extra_options))}")
            
            # Check option values
            for opt in expected_options:
                if opt in user_options and expected_options[opt] != user_options[opt]:
                    feedback_parts.append(f"Incorrect value for -{opt}. Expected: {expected_options[opt]}, got: {user_options[opt]}")
        
        if not feedback_parts:
            feedback_parts.append("Check your command syntax and arguments.")
        
        return ". ".join(feedback_parts) + "."
    
    def get_introduction(self) -> str:
        """Return introduction to ssh command."""
        return """
The 'ssh' command is used for secure remote login and command execution. It's essential for system administration and secure communications.

Common options:
- ssh user@host           : Basic connection
- ssh -p PORT user@host   : Connect to specific port
- ssh -i keyfile user@host: Use specific private key
- ssh -v user@host        : Verbose output for debugging
- ssh -X user@host        : Enable X11 forwarding
- ssh -A user@host        : Enable agent forwarding
- ssh -L port:host:port   : Local port forwarding (tunnel)
- ssh -R port:host:port   : Remote port forwarding
- ssh -D port user@host   : Dynamic port forwarding (SOCKS proxy)
- ssh -J jump@host        : Use jump host (ProxyJump)
- ssh -f user@host        : Run in background
- ssh -N user@host        : Don't execute remote commands
- ssh -C user@host        : Enable compression
- ssh -o option user@host : Set SSH options
- ssh -F configfile       : Use specific config file
- ssh -4/-6 user@host     : Force IPv4/IPv6
- ssh -q user@host        : Quiet mode
- ssh -c cipher user@host : Specify cipher
- ssh -m mac user@host    : Specify MAC algorithm

Advanced usage:
- ControlMaster/ControlPath: Connection multiplexing
- ProxyCommand: Custom connection methods
- ProxyJump (-J): Simplified jump host syntax
- Multiple tunnels: Use multiple -L/-R options
- Escape sequences: Use -e to change escape character

Security tips:
- Always verify host keys on first connection
- Use key-based authentication when possible
- Avoid password authentication for production systems
- Use non-standard ports when possible
- Enable compression for slow links
- Use agent forwarding carefully (security risk)
        """
