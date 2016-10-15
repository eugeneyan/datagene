require 'spec_helper'


describe Axis do
  it 'should have a name' do
    axes = Axis.all

    axes.each do |axis|
      axis.name.should_not be_nil
      axis.name.should_not == ''
    end
  end


  it 'should have 5 active axis for each game type' do
    game_types = Axis.select(:game_type).distinct.map { |obj| obj.game_type }
    
    game_types.each do |game_type|
      axes = Axis.active.where(game_type: game_type)
      axes.count.should == 5
    end
  end


  it 'should have one axis holding one of the values(1..5) for each game type' do
    game_types = Axis.select(:game_type).distinct.map { |obj| obj.game_type }
    
    game_types.each do |game_type|
      axes = Axis.active.where(game_type: game_type).order('value ASC')
      axes.each_with_index do |axis, index|
        axis.value.should == index + 1
      end
    end
  end
end