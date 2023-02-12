#     Copyright 2020. Ticos
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

CURRENT_VERSION=$( grep -Po 'VERSION[ ,]=[ ,]\"\K(([0-9])+(\.){0,1})+' setup.py )
if [ "$1" = "clean" ] || [ "$1" = "only_clean" ] ; then
  sudo rm -rf /var/log/ticos-gateway/
  sudo rm -rf deb_dist/
  sudo rm -rf dist/
  sudo rm -rf ticos-gateway.egg-info/
  sudo rm -rf /etc/ticos-gateway/
  sudo rm -rf ticos-gateway-$CURRENT_VERSION.tar.gz
  sudo rm -rf ticos-gateway-$CURRENT_VERSION.deb
  sudo rm -rf python3-ticos-gateway.deb
  sudo rm -rf python3-ticos-gateway.rpm
  sudo rm -rf ticos-gateway-$CURRENT_VERSION.noarch.rpm
  sudo rm -rf ticos_gateway.egg-info
  sudo rm -rf /home/zenx/rpmbuild/BUILDROOT/*
  sudo rm -rf build/
  sudo rm -rf docker/config || echo ''
  sudo rm -rf docker/extensions || echo ''
  sudo find ticos_gateway/ -name "*.pyc" -exec rm -f {} \;
  sudo apt remove python3-ticos-gateway -y
fi


CURRENT_USER=$USER
export PYTHONDONTWRITEBYTECODE=1

if [ "$1" != "only_clean" ] ; then
  echo "Building DEB package"
  # Create sources for DEB package
  python3 setup.py --command-packages=stdeb.command bdist_deb
  #find ticos_gateway/ -name "*.pyc" -exec rm -f {} \;
  echo 1
  # Adding the files, scripts and permissions
  cp -r for_build/etc deb_dist/ticos-gateway-$CURRENT_VERSION/debian/python3-ticos-gateway
  cp -r for_build/var deb_dist/ticos-gateway-$CURRENT_VERSION/debian/python3-ticos-gateway
  cp -r -a for_build/DEBIAN deb_dist/ticos-gateway-$CURRENT_VERSION/debian/python3-ticos-gateway
  chown root:root deb_dist/ticos-gateway-$CURRENT_VERSION/debian/python3-ticos-gateway/ -R
  chown root:root deb_dist/ticos-gateway-$CURRENT_VERSION/debian/python3-ticos-gateway/var/ -R
  chmod 775 deb_dist/ticos-gateway-$CURRENT_VERSION/debian/python3-ticos-gateway/DEBIAN/preinst
  chmod +x deb_dist/ticos-gateway-$CURRENT_VERSION/debian/python3-ticos-gateway/DEBIAN/postinst
  chown root:root deb_dist/ticos-gateway-$CURRENT_VERSION/debian/python3-ticos-gateway/DEBIAN/preinst
# Bulding Deb package
  dpkg-deb -b deb_dist/ticos-gateway-$CURRENT_VERSION/debian/python3-ticos-gateway/
  mkdir deb-temp
  cd deb-temp
  ar x ../deb_dist/ticos-gateway-$CURRENT_VERSION/debian/python3-ticos-gateway.deb
  zstd -d *.zst
  rm *.zst
  xz *.tar
  ar r ../python3-ticos-gateway.deb debian-binary control.tar.xz data.tar.xz
  cd ..
  rm -r deb-temp
  # Create sources for RPM Package
  echo 'Building RPM package'
  #find ticos_gateway/ -name "*.pyc" -exec rm -f {} \;
  python3 setup.py bdist_rpm
  #find ticos_gateway/ -name "*.pyc" -exec rm -f {} \;
  cp build/bdist.linux-x86_64/rpm/* /home/$CURRENT_USER/rpmbuild/ -r
  # Adding the file, scripts and permissions
  cp for_build/etc/systemd/system/ticos-gateway.service /home/$CURRENT_USER/rpmbuild/SOURCES/
  cp -r ticos_gateway/extensions for_build/etc/ticos-gateway/
  cd for_build/etc/ticos-gateway || echo 0 > /dev/null
  tar -zcvf configs.tar.gz config/*
  tar -zcvf extensions.tar.gz extensions/*
  mv configs.tar.gz ../../../ -f
  cd ../../../
  rm /home/$CURRENT_USER/rpmbuild/SOURCES/configs.tar.gz
  cp configs.tar.gz /home/$CURRENT_USER/rpmbuild/SOURCES/
  # Bulding RPM Package
  cp ticos-gateway.spec /home/$CURRENT_USER/rpmbuild/SPECS/
  rpmbuild -ba ticos-gateway.spec
  cp /home/$CURRENT_USER/rpmbuild/RPMS/noarch/*.rpm .
  mv ticos-gateway-$CURRENT_VERSION-1.noarch.rpm python3-ticos-gateway.rpm
  chown $CURRENT_USER. *.rpm
fi
