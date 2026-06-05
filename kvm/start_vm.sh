#!/bin/bash -e

DISK_SIZE="100G"
MEMORY="8192"
VCPUS="2"

# Arch
VM_NAME="arch1"
file="Arch-Linux-x86_64-cloudimg.qcow2"
url="https://fastly.mirror.pkgbuild.com/images/latest/$file"
OSINFO="archlinux"

# Ubuntu 24.04
# VM_NAME="openclaw"
# file="noble-server-cloudimg-amd64.img"
# url="https://cloud-images.ubuntu.com/noble/current/$file"
# OSINFO="ubuntu24.04"

PUBLIC_KEY="$HOME/.ssh/id_ed25519.pub"
INSTANCE_ID="${VM_NAME}-$(date +%Y%m%d%H%M%S)-$(uuidgen | cut -d- -f1)"
LOCAL_HOSTNAME="$VM_NAME"
TIMEOUT=180 # Seconds to wait for it to come up & get a dhcp address
SSH_TIMEOUT=180 # Seconds to wait retrying SSH

# Ensure we have the public ssh key ready to go
ls $PUBLIC_KEY

# Ensure Ubuntu thinks we're OK to run KVM
sudo apt-get update
sudo apt-get install -y cpu-checker
kvm-ok

# Install deps
sudo apt-get install -y qemu-kvm libvirt-daemon-system libvirt-clients virtinst qemu-utils cloud-image-utils libnss-libvirt

temp_dir=$(mktemp -d)
echo "Temporary directory: $temp_dir"
cd $temp_dir

# Get the image
if [ ! -f "$file" ]; then
  wget "$url"
fi

# Convert the image
if [[ "$file" != *.qcow2 ]]; then
    newfile="${file%.*}.qcow2"
    qemu-img convert -O qcow2 "$file" "$newfile"
    file="$newfile"
fi

# Resize the image and copy it into place
qemu-img resize $file $DISK_SIZE
sudo mv $file /var/lib/libvirt/images/
sudo chown libvirt-qemu:kvm /var/lib/libvirt/images/$file

# Create config files
cat > user-data <<'EOF'
#cloud-config
users:
  - name: vmadmin
    groups: [sudo]
    shell: /bin/bash
    sudo: ["ALL=(ALL) NOPASSWD:ALL"]
    ssh_authorized_keys:
      - REPLACE_WITH_YOUR_PUBLIC_SSH_KEY
ssh_pwauth: false
disable_root: true
package_update: true
packages:
  - qemu-guest-agent
runcmd:
  - systemctl enable --now qemu-guest-agent
EOF

PUBKEY="$(cat $PUBLIC_KEY)"
sed -i "s|REPLACE_WITH_YOUR_PUBLIC_SSH_KEY|$PUBKEY|" user-data

echo "instance-id: $INSTANCE_ID" > meta-data
echo "local-hostname: $LOCAL_HOSTNAME" >> meta-data

# Boot the VM
virt-install \
  --connect qemu:///system \
  --name $LOCAL_HOSTNAME \
  --memory $MEMORY \
  --vcpus $VCPUS \
  --osinfo $OSINFO \
  --import \
  --disk path=/var/lib/libvirt/images/$file,format=qcow2,bus=virtio \
  --network network=default,model=virtio \
  --graphics none \
  --noautoconsole \
  --cloud-init user-data=user-data,meta-data=meta-data

deadline=$((SECONDS + TIMEOUT))
ip=""

while (( SECONDS < deadline )); do
  ip="$(
    virsh -c qemu:///system domifaddr "$VM_NAME" --source lease 2>/dev/null |
      awk '$3 == "ipv4" { sub(/\/.*/, "", $4); print $4; exit }'
  )"

  if [[ -n "$ip" ]]; then
    break
  fi

  sleep 2
done

if [[ -z "$ip" ]]; then
  echo "Timed out waiting for DHCP lease for $VM_NAME" >&2
  exit 1
fi

echo "VM IP is $ip"

# SSH and wait for cloud-init
deadline=$((SECONDS + SSH_TIMEOUT))

until ssh \
  -o BatchMode=yes \
  -o ConnectTimeout=5 \
  -o StrictHostKeyChecking=accept-new \
  "vmadmin@$ip" \
  'true'
do
  if (( SECONDS >= deadline )); then
    echo "Timed out waiting for SSH on $ip" >&2
    exit 1
  fi

  sleep 2
done

ssh "vmadmin@$ip" 'cloud-init status --wait'

echo "cloud-init completed on $ip"

echo 'MANUAL: Edit /etc/nsswitch.conf to add "libvirt" and "libvirt_guest" before "dns" to the "hosts:" line.'

echo "VM is up. Helpful commands:"
echo "virsh -c qemu:///system list --all"
echo "virsh -c qemu:///system start $VM_NAME"
echo "virsh -c qemu:///system shutdown $VM_NAME"
echo "virsh -c qemu:///system reboot $VM_NAME"
echo "virsh -c qemu:///system console $VM_NAME"
echo "virsh -c qemu:///system autostart $VM_NAME"
echo "virsh -c qemu:///system dominfo $VM_NAME"
echo "ssh vmadmin@$LOCAL_HOSTNAME"
echo "# virsh -c qemu:///system undefine $VM_NAME --remove-all-storage"
