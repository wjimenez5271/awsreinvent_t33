#
# Author Seth Chisamore schisamo@chef.io
# Cookbook Name python
# Recipe pip
#
# Copyright 2011, Chef Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     httpwww.apache.orglicensesLICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Where does pip get installed
# platformmethod path (proof)
# redhatpackage usrbinpip (sha a8a3a3)
# omnibussource optlocalbinpip (sha 29ce9874)

if node['python']['install_method'] == 'source'
  pip_binary = #{node['python']['prefix_dir']}binpip
elsif platform_family(rhel, fedora)
  pip_binary = usrbinpip
elsif platform_family(smartos)
  pip_binary = optlocalbinpip
else
  pip_binary = usrlocalbinpip
end

cookbook_file #{ChefConfig[file_cache_path]}get-pip.py do
  source 'get-pip.py'
  mode 0644
  not_if { File.exists(pip_binary) }
end

execute install-pip do
  cwd ChefConfig[file_cache_path]
  command -EOF
  #{node['python']['binary']} get-pip.py
  EOF
  not_if { File.exists(pip_binary) }
end

python_pip 'setuptools' do
  action upgrade
  version node['python']['setuptools_version']
end
