require 'spec_helper'

describe Skill do
  # This test checks if the database is populated
  # 50 is an arbitrary chosen value to check data is populated
  it 'should have more than or equal to 50 active skills in the database' do
    Skill.active.count.should be >= 50
  end


  it 'should have a name' do
    skills = Skill.all

    skills.each do |skill|
      skill.name.should_not be_nil
      skill.name.should_not == ''
    end
  end


  it 'should have a description' do
    skills = Skill.all

    skills.each do |skill|
      skill.description.should_not be_nil
      skill.description.should_not == ''
    end
  end
end
