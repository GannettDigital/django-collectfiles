require "open3"

Given(/^I have apps with "(.*?)" directories$/) do |source_dir|
  @source_dir = source_dir
end

When(/^I run the collectfiles command/) do
  @out_dir = "features/out/#{@source_dir}-root"
  cmd = "
    rm -rf #{@out_dir}
    DJANGO_SETTINGS_MODULE=example.settings django-admin.py collectfiles #{@out_dir} #{@source_dir} 
    "
  raise unless system(cmd)
end

Then(/^the app directories should be collected as expected$/) do
  expected = "features/expected/#{@source_dir}-root"
  raise unless system("diff -r '#{@out_dir}' '#{expected}'")
end
