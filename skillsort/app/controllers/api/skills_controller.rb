module Api
  class SkillsController < ApplicationController


    def index
      @skills = Skill.active.select( 'id, name, description' )
      render json: @skills, status: 200
    end
  end
end