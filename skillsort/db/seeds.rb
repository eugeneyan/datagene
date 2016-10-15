require 'csv'

# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)

# Prompt to clean database
# print "CAUTION: This will erase all data and re-populate with seed data. Proceed (y/n) ? "
# response = gets.chomp

# Delete all skills and create Skills seed data from skills_yyyymmdd.csv file.
Skill.delete_all

skills_file = 'skills_20140208.csv';
CSV.foreach("./db/skills/#{skills_file}", headers: true) do |row|
	Skill.create( id: row[0], name: row[1], description: row[2], active: true )
end

# Delete all Axis and create Axis seed data from axis_yyyymmdd.csv file.
Axis.delete_all

axis_file = 'axis_20140326.csv'
CSV.foreach("./db/axis/#{axis_file}", headers: true) do |row|
	Axis.create( id: row[0], name: row[1], description: row[2], value: row[3], active: row[4], game_type: row[5] )
end

# Delete all Industries and create Industry seed data from axis_yyyymmdd.csv file.
Industry.delete_all

industry_file = 'industries_20140309.csv'
CSV.foreach("./db/industry/#{industry_file}", headers: true) do |row|
	Industry.create( id: row[0], name: row[1], active: row[2] )
end

# Delete all Industries and create Industry seed data from axis_yyyymmdd.csv file.
Function.delete_all

function_file = 'functions_20140309.csv'
CSV.foreach("./db/function/#{function_file}", headers: true) do |row|
	Function.create( id: row[0], name: row[1], active: row[2] )
end

# Delete all Countries and create Country seed data from countries_yyyymmdd.csv file.
Country.delete_all

country_file = 'countries_20140405.csv'
CSV.foreach("./db/country/#{country_file}", headers: true) do |row|
	Country.create( id: row[0], name: row[1], active: row[2] )
end