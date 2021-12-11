package com.pubsub.gcp.publisher;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonSetter;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import lombok.*;

@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor
@JsonSerialize
@JsonIgnoreProperties(ignoreUnknown = true)
public class ProductData {
    //public Long id;
    public String CONSOLE;
    public String PUBLISHER;
    public Double CRITICS_POINTS;
    public String CATEGORY;
    public String RATING;
    public Integer USER_POINTS;
    public Integer YEAR;

    @JsonSetter("CONSOLE")
    public void setCONSOLE(String CONSOLE) {
        this.CONSOLE = CONSOLE;
    }

    @JsonSetter("PUBLISHER")
    public void setPUBLISHER(String PUBLISHER) {
        this.PUBLISHER = PUBLISHER;
    }

    @JsonSetter("CRITICS_POINTS")
    public void setCRITICS_POINTS(Double CRITICS_POINTS) {
        this.CRITICS_POINTS = CRITICS_POINTS;
    }

    @JsonSetter("CATEGORY")
    public void setCATEGORY(String CATEGORY) {
        this.CATEGORY = CATEGORY;
    }

    @JsonSetter("RATING")
    public void setRATING(String RATING) {
        this.RATING = RATING;
    }

    @JsonSetter("USER_POINTS")
    public void setUSER_POINTS(Integer USER_POINTS) {
        this.USER_POINTS = USER_POINTS;
    }

    @JsonSetter("YEAR")
    public void setYEAR(Integer YEAR) {
        this.YEAR = YEAR;
    }
}
