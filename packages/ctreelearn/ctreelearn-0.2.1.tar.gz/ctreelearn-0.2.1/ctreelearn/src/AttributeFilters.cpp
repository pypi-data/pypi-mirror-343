
#include "../include/AttributeFilters.hpp"


    AttributeFilters::AttributeFilters(MorphologicalTreePtr tree){
        this->tree = tree;
    }

    AttributeFilters::~AttributeFilters(){
        
    }
                           
    ImagePtr AttributeFilters::filteringByPruningMin(float* attribute, float threshold){
        ImagePtr imgOutput = Image::create(this->tree->getNumRowsOfImage(), this->tree->getNumColsOfImage());
        AttributeFilters::filteringByPruningMin(this->tree, attribute, threshold, imgOutput->rawData());
        return imgOutput;
    }

    ImagePtr AttributeFilters::filteringByPruningMax(float* attribute, float threshold){
        ImagePtr imgOutput = Image::create(this->tree->getNumRowsOfImage(), this->tree->getNumColsOfImage());
        AttributeFilters::filteringByPruningMax(this->tree, attribute, threshold, imgOutput->rawData());
        return imgOutput;
    }

    ImagePtr AttributeFilters::filteringByPruningMin(std::vector<bool>& criterion){
        ImagePtr imgOutput = Image::create(this->tree->getNumRowsOfImage(), this->tree->getNumColsOfImage());
        AttributeFilters::filteringByPruningMin(this->tree, criterion, imgOutput->rawData());
        return imgOutput;
    }

    ImagePtr AttributeFilters::filteringByDirectRule(std::vector<bool>& criterion){
        ImagePtr imgOutput = Image::create(this->tree->getNumRowsOfImage(), this->tree->getNumColsOfImage());
        AttributeFilters::filteringByDirectRule(this->tree, criterion, imgOutput->rawData());
        return imgOutput;
    }

    ImagePtr AttributeFilters::filteringByPruningMax(std::vector<bool>& criterion){
        ImagePtr imgOutput = Image::create(this->tree->getNumRowsOfImage(), this->tree->getNumColsOfImage());

        AttributeFilters::filteringByPruningMax(this->tree, criterion, imgOutput->rawData());

        return imgOutput;

    }

    ImagePtr AttributeFilters::filteringBySubtractiveRule(std::vector<bool>& criterion){

        ImagePtr imgOutput = Image::create(this->tree->getNumRowsOfImage(), this->tree->getNumColsOfImage());
        AttributeFilters::filteringBySubtractiveRule(this->tree, criterion, imgOutput->rawData());

        return imgOutput;

    }

    float* AttributeFilters::filteringBySubtractiveScoreRule(float* prob){
        int n = this->tree->getNumRowsOfImage() * this->tree->getNumColsOfImage();
        float* imgOutput = new float[n];

        AttributeFilters::filteringBySubtractiveScoreRule(this->tree, prob, imgOutput);

        return imgOutput;

    }

   
