Feature: collectfiles
  As a application developer,
  I want to collect all features files from the application

Scenario: collect features
  Given I have apps with "features" directories
  When I run the collectfiles command
  Then the app directories should be collected as expected

