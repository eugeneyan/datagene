require 'spec_helper'

describe Country do
  # This test checks if the database is populated
  # 200 is an arbitrary chosen value to check data is populated
  it 'should have more than or equal to 200 active countries in the database' do
    Country.active.count.should be >= 200
  end


  it 'should have a name' do
    countries = Country.all

    countries.each do |country|
      country.name.should_not be_nil
      country.name.should_not == ''
    end
  end
end